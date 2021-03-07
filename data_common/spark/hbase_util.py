# encoding=utf-8
import json
import xmltodict


class HbaseConf:

    """
    定义hbase标准数据格式：
    (row_key, {"f1:c1": "v1", "f1:c2": "v2", "f2:c3": "v3", "f2:c4": c4})
    例如：
    ('0001', {'data:grade': '7-1', 'data:school': 'SZZX', 'info:name': 'Tom', 'info:sex': 'male'})
    """

    @staticmethod
    def get_xml_to_dict(xml_path):
        with open(xml_path, encoding='utf-8') as fp:
            xml_obj = xmltodict.parse(fp.read())
            string = json.dumps(xml_obj)
            return json.loads(string)

    @staticmethod
    def get_hbase_conf(suffix=''):
        xml_list = [f'core-site{suffix}.xml', f'hdfs-site{suffix}.xml',
                    f'yarn-site{suffix}.xml', f'hbase-site{suffix}.xml']
        conf_all = {}
        import os
        for xml_path in xml_list:
            xml_path = os.path.dirname(__file__) + '/conf/' + xml_path
            conf = HbaseConf.get_xml_to_dict(xml_path)
            properties = conf.get('configuration', {}).get('property')
            properties = properties if isinstance(properties, list) else [properties]
            for property in properties:
                conf_all[property['name']] = property['value']
        return conf_all

    @staticmethod
    def spark_hbase_read_format(row):
        """
        data = ('0001', '{"qualifier" : "grade", "timestamp" : "1597600074297", "columnFamily" : "data", "row" : "0001", "type" : "Put", "value" : "7-1"}\n{"qualifier" : "school", "timestamp" : "1597600099790", "columnFamily" : "data", "row" : "0001", "type" : "Put", "value" : "SZZX"}\n{"qualifier" : "name", "timestamp" : "1597600001433", "columnFamily" : "info", "row" : "0001", "type" : "Put", "value" : "Tom"}\n{"qualifier" : "sex", "timestamp" : "1597600029796", "columnFamily" : "info", "row" : "0001", "type" : "Put", "value" : "male"}')
        将spark读取hbase的记录，是json行数据,转换成标准格式数据
        ('0001', {'data:grade': '7-1', 'data:school': 'SZZX', 'info:name': 'Tom', 'info:sex': 'male'})
        :param row:
        :return:
        """
        row_key, lines = row[0], row[1]
        lines = [json.loads(line) for line in lines.split('\n')]
        row_data = {}
        for line in lines:
            family = line['columnFamily']
            column = line['qualifier']
            value = line['value']
            timestamp = line['timestamp']
            row_data[f'{family}:{column}'] = value
            # row_data[f'{family}:{column}:timestamp'] = timestamp
        return row_key, row_data

    @staticmethod
    def spark_hbase_write_format(row):
        """
        将标准格式数据，转换成spark存储hbase的数据格式
        ('0001', {'data:grade': '7-1', 'data:school': 'SZZX', 'info:name': 'Tom', 'info:sex': 'male'})
        转换成：
        [('0001', ['0001', 'data', 'grade', '7-1']),
         ('0001', ['0001', 'data', 'school', 'SZZX']),
         ('0001', ['0001', 'info', 'name', 'Tom']),
         ('0001', ['0001', 'info', 'sex', 'male'])]
        :param row:
        :return:
        """
        row_key, row_data = row[0], row[1]
        lines = []
        for key, value in row_data.items():
            if 'timestamp' in key:
                continue
            family = key.split(':')[0]
            column = key.split(':')[1]
            line = (row_key, [row_key, family, column, value])
            lines.append(line)
        return lines

    @staticmethod
    def dict2row(row_key, row_data):
        """
        将字典格式转换成标准格式
        ('0001', {'info': {'name': 'Jack', 'sex': 'female'}, 'data': {'school': 'SXZX-1', 'grade': '7-2'}}),
        转换成：
        ('0001', {'data:grade': '7-1', 'data:school': 'SZZX', 'info:name': 'Tom', 'info:sex': 'male'})

        py_hbase_insert_list = []
        spark_hbase_insert_list = []
        for item in data:
            row = HbaseConf.dict2row(item[0], item[1])
            cells = HbaseConf.convert_write(row)
            py_hbase_insert_list.append(row)
            spark_hbase_insert_list.extend(cells)
        print(py_hbase_insert_list)
        # hb.put_batch('student', py_hbase_insert_list)
        print(spark_hbase_insert_list)
        :param row_key:
        :param row_data:
        :return:
        """
        _dict = {}
        for family, info in row_data.items():
            for key, value in info.items():
                k = f'{family}:{key}'
                _dict[k] = value
        return row_key, _dict

    @staticmethod
    def row2dict(row):
        """
        将标准格式转换成字典格式
        ('0001', {'data:grade': '7-1', 'data:school': 'SZZX', 'info:name': 'Tom', 'info:sex': 'male'})
        转换成：
        ('0001', {'info': {'name': 'Jack', 'sex': 'female'}, 'data': {'school': 'SXZX-1', 'grade': '7-2'}}),
        :param row_key:
        :param row_data:
        :return:
        """
        row_key = row[0]
        row_data = row[1]
        _dict = {}
        for k, v in row_data.items():
            f, c = k.split(':')
            if f not in _dict:
                _dict[f] = {}
            _dict[f][c] = v
        return row_key, _dict

    @staticmethod
    def bytes2str(value, decode='utf-8'):
        if isinstance(value, bytes):
            return value.decode(decode)
        return value

    @staticmethod
    def row_bytes2str(row):
        row_key = HbaseConf.bytes2str(row[0])
        row_data = {HbaseConf.bytes2str(k): HbaseConf.bytes2str(v) for k, v in row[1].items()}
        return row_key, row_data


class HappyHbaseUtil:

    def __init__(self):
        """已经封装了Hbase"""
        self.host = '192.168.131.11'
        self.port = 9090
        self.timeout = 5000
        self.client = None
        self.connect = None
        self.transport = None
        self.connection()

    def connection(self):
        import happybase
        self.connect = happybase.Connection(host=self.host,
                                            port=self.port,
                                            autoconnect=True,
                                            transport='buffered',
                                            protocol='binary')
        self.client = self.connect.client

    def get_table_list(self):
        return [HbaseConf.bytes2str(table) for table in self.connect.tables()]

    def disable_table(self, table):
        """禁用表：在做一些删除操作之前必须先禁用表"""
        self.connect.disable_table(table)

    def enable_table(self, table):
        """启用表"""
        self.connect.enable_table(table)

    def create_table(self, table, family_info):
        """
        falimies = {
                'cf1': dict(max_versions=10),
                'cf2': dict(max_versions=1, block_cache_enabled=False),
                'cf3': dict(),  # use defaults
            }
        :param table:
        :param falimies:
        :return:
        """
        self.connect.create_table(table, family_info)
        return True

    def get_columns_desc(self, table):
        """
        {b'data': {'name': b'data:', 'max_versions': 1, 'compression': b'NONE', 'in_memory': False, 'bloom_filter_type': b'ROW', 'bloom_filter_vector_size': 0, 'bloom_filter_nb_hashes': 0, 'block_cache_enabled': True, 'time_to_live': 2147483647}, b'info': {'name': b'info:', 'max_versions': 1, 'compression': b'NONE', 'in_memory': False, 'bloom_filter_type': b'ROW', 'bloom_filter_vector_size': 0, 'bloom_filter_nb_hashes': 0, 'block_cache_enabled': True, 'time_to_live': 2147483647}}
        :param table:
        :return:
        """
        t = self.connect.table(table)
        info = t.families()
        return info

    def get_columns_desc2(self, table):
        """
        {b'data:': ColumnDescriptor(name=b'data:', maxVersions=1, compression=b'NONE', inMemory=False, bloomFilterType=b'ROW', bloomFilterVectorSize=0, bloomFilterNbHashes=0, blockCacheEnabled=True, timeToLive=2147483647), b'info:': ColumnDescriptor(name=b'info:', maxVersions=1, compression=b'NONE', inMemory=False, bloomFilterType=b'ROW', bloomFilterVectorSize=0, bloomFilterNbHashes=0, blockCacheEnabled=True, timeToLive=2147483647)}
        :param table:
        :return:
        """
        return self.client.getColumnDescriptors(table)

    def get_cells(self, table, row_key, family_column, timestamp=None, include_timestamp=False):
        t = self.connect.table(table)
        cells = t.cells(row_key, family_column, timestamp=timestamp,
                       include_timestamp=include_timestamp)
        return cells

    def get_row(self, table, row_key, columns=None, timestamp=None, include_timestamp=False):
        """
        {b'data:grade': b'7-1', b'data:school': b'SZZX', b'info:name': b'Tom', b'info:sex': b'male'}
        :param table:
        :param row_key:
        :param columns:
        :param timestamp:
        :param include_timestamp:
        :return:
        """
        t = self.connect.table(table)
        info = t.row(row_key, columns=columns, timestamp=timestamp,
                     include_timestamp=include_timestamp)
        return HbaseConf.row_bytes2str((row_key, info))

    def get_row2(self, table, row_key):
        """
        [TRowResult(row=b'0001', columns={b'data:grade': TCell(value=b'7-1', timestamp=1597600074297), b'data:school': TCell(value=b'SZZX', timestamp=1597600099790), b'info:name': TCell(value=b'Tom', timestamp=1597600001433), b'info:sex': TCell(value=b'male', timestamp=1597600029796)}, sortedColumns=None)]
        :param table:
        :param row_key:
        :return:
        """
        return self.client.getRow(table, row_key)

    def put_row(self, table, row_key, data):
        """
        添加数据
        :param table:
        :param row_key:
        :param data: {'family:key1': 'value1','family:key2': 'value2'}
        :return:
        """
        t = self.connect.table(table)
        t.put(row_key, data)
        return True

    def get_batch(self, table, rows):
        """
        :param table:
        :param rows: list, ['row-key1', 'row-key2']
        :return:
        """
        t = self.connect.table(table)
        for row in t.rows(rows):
            yield HbaseConf.row_bytes2str(row)

    def put_batch(self, table, list_data):
        """
        [('row-key1', {'family:key1': 'value1', 'family:key2': 'value2'}),
         ('row-key2'), {'family:key1': 'value1', 'family:key2': 'value2'}]
        :param table:
        :param list_data:
        :return:
        """
        # 批量添加
        t = self.connect.table(table)
        bat = t.batch()
        for row_key, row_data in list_data:
            bat.put(row_key, row_data)
        bat.send()

    def scan(self, table, **kwargs):
        """
        scanner = table.scan(
            row_start=None,
            row_stop=None,
            row_prefix=None,
            columns=None,
            filter=None,
            timestamp=None,
            include_timestamp=False,
            batch_size=1000,
            scan_batching=None,
            limit=None,
            sorted_columns=False,
            reverse=False,
        )
        # row_start：起始行，默认None，即第一行，可传入行号指定从哪一行开始
        # row_stop：结束行，默认None，即最后一行，可传入行号指定到哪一行结束(不获取此行数据)
        # row_prefix：行号前缀，默认为None，即不指定前缀扫描，可传入前缀来扫描符合此前缀的行
        # columns：列，默认为None，即获取所有列，可传入一个list或tuple来指定获取列
        # filter：过滤字符串  SingleColumnValueFilter ('f', 'c1', =, 'binary:val1')
        message SingleColumnValueFilter {
            required ComparatorType comparator = 1;
            required string column_name = 2;
            required bytes column_value = 3;
            required bool filter_if_missing = 4;
            required bool latest_version_only = 5;
        }
        SingleColumnValueFilter(Bytes.toBytes("c1"), Bytes.toBytes("city"), CompareOp.EQUAL, Bytes.toBytes(v1))
        # timestamp：时间戳。默认为None，即返回最大的那个时间戳的数据。可传入一个时间戳来获取小于此时间戳的最大时间戳的版本数据
        # include_timestamp：是否返回时间戳数据，默认为False
        # batch_size：用于检索结果的批量大小
        # scan_batching：服务端扫描批处理
        # limit：数量
        # sorted_columns：是否返回排序的列(根据行名称排序)
        # reverse：是否执行反向扫描

        # 通过row_start和row_stop参数来设置开始和结束扫描的row key
        table.scan(row_start='www.test2.com', row_stop='www.test3.com')
        另外，还可以通过设置row key的前缀来进行局部扫描
        # 通过row_prefix参数来设置需要扫描的row key
        table.scan(row_prefix='www.test')
        :return:
        """
        t = self.connect.table(table)
        for row in t.scan(**kwargs):
            yield HbaseConf.row_bytes2str(row)

    def close(self):
        return self.connect.close()


class HbaseUtil:

    def __init__(self):
        """直接通过Hbase"""
        self.host = '192.168.131.11'
        self.port = 9090
        self.timeout = 5000
        self.client = None
        self.transport = None
        self.connection()

    def connection(self):
        from hbase import Hbase
        from thrift.transport import TSocket, TTransport
        from thrift.protocol import TBinaryProtocol

        # server端地址和端口，web是HMaster也就是thriftServer主机名，thriftServer默认端口是9090
        socket = TSocket.TSocket(self.host, self.port)
        # 可以设置超时
        socket.setTimeout(self.timeout)
        # 设置传输方式（TFramedTransport或TBufferedTransport）
        self.transport = TTransport.TBufferedTransport(socket)
        # 设置传输协议，缺省简单的二进制序列化协议
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(protocol)
        self.transport.open()

    def disable_table(self, name):
        """禁用表：在做一些删除操作之前必须先禁用表"""
        self.client.disableTable(name)

    def enable_table(self, name):
        """启用表"""
        self.client.enableTable(name)

    def create_table(self, name, column_descriptors):
        self.client.createTable(name, column_descriptors)

    def get_table_list(self):
        return self.client.getTableNames()

    def get_columns_desc(self, name):
        return self.client.getColumnDescriptors(name)

    def get_row(self, table, row_key):
        return self.client.getRow(table, row_key)

    def close(self):
        return self.transport.close()


if __name__ == '__main__':
    conf = HbaseConf.get_hbase_conf()
    print(conf)

    hb = HappyHbaseUtil()

    table_names = hb.get_table_list()
    print(table_names)

    res = hb.get_row('student', '0001')
    res2 = hb.get_row2('student', '0001')
    res3 = hb.get_cells('student', '0001', 'info:name')
    print(res)
    print(res2)
    print(res3)
    for row in hb.scan('student'):
        # filter="SingleColumnValueFilter ('data', 'school', =, 'binary:SZZX')"):
        print(row)

    # batch = hb.get_batch('student', ['0003', '0004'])
    # for item in batch:
    #     print(item)

    # [('row-key1', {'family:key1': 'value1', 'family:key2': 'value2'}),
    #  ('row-key2'), {'family:key1': 'value1', 'family:key2': 'value2'}]

    # data = [
    #     ('0004', {'info': {'name': 'Jack', 'sex': 'female'}, 'data': {'school': 'SXZX-1', 'grade': '7-2'}}),
    #     ('0005', {'info': {'name': 'Tony', 'sex': 'male'}, 'data': {'school': 'SXZX-2', 'grade': '7-2'}})
    # ]


    # data = ('0001', '{"qualifier" : "grade", "timestamp" : "1597600074297", "columnFamily" : "data", "row" : "0001", "type" : "Put", "value" : "7-1"}\n{"qualifier" : "school", "timestamp" : "1597600099790", "columnFamily" : "data", "row" : "0001", "type" : "Put", "value" : "SZZX"}\n{"qualifier" : "name", "timestamp" : "1597600001433", "columnFamily" : "info", "row" : "0001", "type" : "Put", "value" : "Tom"}\n{"qualifier" : "sex", "timestamp" : "1597600029796", "columnFamily" : "info", "row" : "0001", "type" : "Put", "value" : "male"}')
    # data_read = HbaseConf.convert_read(data)
    # print(data_read)
    # print(HbaseConf.row2dict(data_read))
    # date_write = HbaseConf.convert_write(data_read)
    # print(date_write)

    # d = [('0001', ['0001', 'data', 'grade', '7-1']),
    #      ('0001', ['0001', 'data', 'school', 'SZZX']),
    #      ('0001', ['0001', 'info', 'name', 'Tom']),
    #      ('0001', ['0001', 'info', 'sex', 'male'])]
