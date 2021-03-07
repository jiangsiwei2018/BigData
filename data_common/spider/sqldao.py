# encoding=utf-8
import time
import pymysql
from data_common.designs.singleton import SingletonType
from data_common.designs.decorator import retry
from data_common.utils.log_util import logger_exception, Logger


class SqlUtil(metaclass=SingletonType):

    where_dict = {
        '$in': 'IN', '$like': 'LIKE',
        '$eq': '=', '$reg': 'REGEXP',
        '$ge': '>=', '$le': '<=',
        '$gt': '>', '$lt': '<'
    }

    CREATE_DATABASE = 'CREATE DATABASE IF NOT EXISTS {database}'
    CREATE_TABLE = 'CREATE TABLE {table} ({keys}, UNIQUE INDEX({index}))'
    CREATE_INDEX = 'CREATE INDEX {index} ON {table}'
    INSERT_TABLE = 'INSERT INTO {table} ({keys}) VALUES ({values})'
    DELETE_TABLE = 'DELETE FROM {table} WHERE {where}'
    UPDATE_TABLE = 'UPDATE {table} SET {update} WHERE {where}'
    # UPDATE_TABLE_ALL = 'UPDATE {table} SET {update}'
    SELECT_TABLE = 'SELECT {keys} FROM {table} WHERE {where}'
    SELECT_TABLE_ALL = 'SELECT * FROM {table} WHERE {where}'
    # INSERT_TABLE_UPDATE = 'INSERT INTO {table} {keys} VALUES {values} ON DUPLICATE KEY UPDATE {update}'

    MAX_RETRY_TIMES = 3

    def __init__(self, ip, port, user, password, database, charset='utf-8'):
        """
        @functions：__init__
        @param： ip, 端口号, 用户名, 用户密码, 数据库编码
        @return：none
        @summary: 初始化类参数, 获取数据库对应的数据库名即对应参数
        """

        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect = None
        self.cursor = None
        self.connected = False
        self.connection()

    def check(self):
        try:
            self.connect.ping()
            return True
        except:
            logger_exception()
            Logger.error('Server not available!')
            self.close()
            return self.connection()

    @retry(3)
    def connection(self):
        """
        @functions：connect
        @param： none
        @return:  如果连接正常,返回True; 否则返回 False
        @summary: 连接数据库
        @error desover:
             解决error --- client does not support authentication
             mysql> alter user 'root'@'localhost' identified with mysql_native_password by '123456';
             Query OK, 0 rows affected (0.10 sec)
             mysql> flush privileges;
            Query OK, 0 rows affected (0.01 sec)
        """
        self.connect = pymysql.connect(host=self.ip, port=self.port,
                                       user=self.user, passwd=self.password,
                                       db=self.database)
        self.cursor = self.connect.cursor()
        self.connect.ping()
        return True

    def close(self):
        try:
            self.connect.close()
        except:
            pass

    def mogrify(self, sql, data=None):
        """sql防注入用法"""
        return self.cursor.mogrify(sql, data)

    @retry(3)
    def command(self, sql, data=[], find=False, _dict=True, _log=True):
        if _log:
            Logger.debug(sql)
        if self.check():
            if _dict:
                cur = self.connect.cursor(pymysql.cursors.DictCursor)
            else:
                cur = self.connect.cursor()
            if data:
                cur.executemany(sql, data)
            else:
                cur.execute(sql)
            results = cur.fetchall()
            cur.close()
            self.connect.commit()
            if find:
                return results
            return True

    @retry(3)
    def insert(self, table, value_list):
        if not value_list:
            return 0
        value_list = value_list if isinstance(value_list, list) else value_list
        keys, place, values = self.convert_insert_data(value_list)
        sql = self.mogrify(SqlUtil.INSERT_TABLE.format(table=table, keys=keys, values=place))
        return self.command(sql, data=values)

    def find(self, table, where={}, keys=[], multi=True):
        w_keys, w_place, w_values = self.convert_where_data(where)
        if keys:
            sql = SqlUtil.SELECT_TABLE.format(table=table, keys=keys, where=w_place)
        else:
            sql = self.mogrify(SqlUtil.SELECT_TABLE_ALL.format(table=table, where=w_place), w_values)
        sql = self.mogrify(sql) if not multi else self.mogrify(sql) + ' limit 1'
        return self.command(sql, find=True)

    def exists(self, table, _id):
        return self.find(table=table, where={'id': _id}, multi=False)

    def update(self, table, update, where):
        u_keys, u_place, u_values = self.convert_where_data(update)
        w_keys, w_place, w_values = self.convert_where_data(where)
        sql = SqlUtil.UPDATE_TABLE.format(table=table, update=u_place, where=w_place)
        sql = self.mogrify(sql, u_values + w_values)
        return self.command(sql)

    def delete(self, table, where):
        w_keys, w_place, w_values = self.convert_where_data(where)
        sql = SqlUtil.DELETE_TABLE.format(table=table, where=w_place)
        sql = self.mogrify(sql, w_values)
        return self.command(sql)

    def is_exists_table(self, table, database=None):
        database = database if database else self.database
        sql = f'show tables from {database};'
        table_list = self.command(sql, find=True)
        table_list = [table[f'Tables_in_{database}'] for table in table_list]
        return True if table in table_list else False

    @retry(3)
    def callproc(self, procname, args):
        """
        @functions: callproc
        @params procname: 存储过程函数名
        @params args: 存储过程参数
        @return: True if excute sucessfully else False
        @summary: 执行存储过程
        """
        if self.check():
            cur = self.connect.cursor()
            cur.callproc(procname, args)
            cur.close()
            self.connect.commit()

    @staticmethod
    def convert_insert_data(value_list):
        if not value_list:
            return [], [], []
        keys = tuple(value_list[0].keys())
        place = tuple(['%s'] * len(keys))
        values = []
        for item in value_list:
            value = list()
            for k in keys:
                value.append(item[k])
            values.append(tuple(value))
        return ', '.join(keys), ', '.join(place), values

    @staticmethod
    def convert_where_data(where, _and=' and '):
        """"
        where={'age': {'$gt': 20}, 'name':'Jim'}
        name=%s and age>%s
        """
        keys = []
        where_keys = []
        where_vals = []
        for k, v in where.items():
            _k = k
            _v = v
            _join = '='
            if isinstance(_v, dict):
                for kk, vv in _v.items():
                    _join = SqlUtil.where_dict.get(kk, '=')
                    _v = vv
            where_keys.append(f'{_k}{_join}%s')
            where_vals.append(_v)
            keys.append(_k)
        place = _and.join(where_keys)
        values = tuple(where_vals)
        return ', '.join(keys), place, values
