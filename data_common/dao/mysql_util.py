# encoding=utf-8
import pymysql
from DBUtils.PersistentDB import PersistentDB
from DBUtils.PooledDB import PooledDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
    not_trans_opt = ['SELECT', 'SHOW', 'DESC']

    CREATE_DATABASE = 'CREATE DATABASE IF NOT EXISTS {database}'
    CREATE_TABLE = 'CREATE TABLE {table} ({keys}, UNIQUE INDEX({index}))'
    CREATE_INDEX = 'CREATE INDEX {index} ON {table}'
    INSERT_TABLE = 'INSERT INTO {table} ({keys}) VALUES ({values})'
    DELETE_TABLE = 'DELETE FROM {table} WHERE {where}'
    UPDATE_TABLE = 'UPDATE {table} SET {update} WHERE {where}'
    SELECT_TABLE = 'SELECT {calc_rows} {keys} FROM {table} WHERE {where}'
    # INSERT_TABLE_UPDATE = 'INSERT INTO {table} {keys} VALUES {values} ON DUPLICATE KEY UPDATE {update}'

    MAX_RETRY_TIMES = 3

    def __init__(self, host, port, user, password, database, charset='utf-8'):
        """
        @functions：__init__
        @param： ip, 端口号, 用户名, 用户密码, 数据库编码
        @return：none
        @summary: 初始化类参数, 获取数据库对应的数据库名即对应参数
        """
        self.config = dict(host=host, port=port, user=user,
                           passwd=password, db=database)
        self.database = database
        self.charset = charset
        self.cursor = None

    def connection(self):
        connect = pymysql.connect(**self.config)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        return connect, cursor

    def mogrify(self, sql, data=None):
        """sql防注入用法"""
        return self.cursor.mogrify(sql, data)

    def trans_opt(self, sql):
        return sql.split(' ')[0].upper() not in self.not_trans_opt

    @retry(3)
    def command(self, sql, data=None, calc_rows=False):
        connect, cursor = self.connection()
        results = []
        row_count = 0
        trans_opt = self.trans_opt(sql)
        try:
            if sql.split(' ')[0].upper() == 'INSERT':
                Logger.debug(sql)
                row_count = cursor.executemany(sql, data)
            else:
                sql = cursor.mogrify(sql, data)
                Logger.debug(sql)
                row_count = cursor.execute(sql)

            if trans_opt:
                connect.commit()
            else:
                results = cursor.fetchall()
            if calc_rows:
                cursor.execute("SELECT FOUND_ROWS() as total")
                rows = cursor.fetchall()
                row_count = rows[0].get('total', 0)
        except:
            if trans_opt:
                connect.rollback()
            logger_exception()
        finally:
            cursor.close()
            connect.close()
        if calc_rows:
            return results, row_count
        return row_count if trans_opt else results

    @retry(3)
    def insert(self, table, value_list):
        if not value_list:
            return 0
        value_list = value_list if isinstance(value_list, list) else value_list
        keys, place, values = self.convert_insert_data(value_list)
        sql = SqlUtil.INSERT_TABLE.format(table=table, keys=self.convert_keys(keys), values=place)
        return self.command(sql, values)

    def find(self, table, where={}, keys=None, calc_rows=True, multi=True,
             other=None, group=None, order=None, limit=0, offset=0):
        w_keys, w_place, w_values = self.convert_where_data(where)
        sql = SqlUtil.SELECT_TABLE.format(table=table,
                                          calc_rows="SQL_CALC_FOUND_ROWS" if calc_rows else "",
                                          keys=self.convert_keys(keys) if keys else "*",
                                          where=w_place)
        if other:
            sql += other
        if group:
            sql += f'GROUP BY {group}'
        if order:
            if not isinstance(order, dict):
                order = {'key': order, 'reverse': 'DESC'}
            sql += f"ORDER BY {order.get('key')} {order.get('reverse', 'DESC')}"
        if not multi:
            sql =  sql + ' limit 1'
        if limit:
            sql = sql + f' LIMIT {limit}'
            if offset:
                sql = sql + f' OFFSET {offset}'
        return self.command(sql, w_values, calc_rows)

    def exists(self, table, _id):
        if self.find(table=table, where={'id': _id}, multi=False):
            return True
        return False

    def update(self, table, update, where):
        u_keys, u_place, u_values = self.convert_where_data(update)
        w_keys, w_place, w_values = self.convert_where_data(where)
        sql = SqlUtil.UPDATE_TABLE.format(table=table, update=u_place, where=w_place)
        return self.command(sql, u_values + w_values)

    def delete(self, table, where):
        w_keys, w_place, w_values = self.convert_where_data(where, ', ')
        sql = SqlUtil.DELETE_TABLE.format(table=table, where=w_place)
        return self.command(sql, w_values)

    def is_exists_table(self, table, database=None):
        database = database if database else self.database
        sql = f'show tables from {database};'
        table_list = self.command(sql)
        table_list = [table[f'Tables_in_{database}'] for table in table_list]
        return True if table in table_list else False

    @retry(3)
    def call_proc(self, procname, args):
        """
        @functions: callproc
        @params procname: 存储过程函数名
        @params args: 存储过程参数
        @return: True if excute sucessfully else False
        @summary: 执行存储过程
        """
        connect, cursor = self.connection()
        try:
            cursor.callproc(procname, args)
            cursor.close()
            connect.commit()
        except:
            connect.rollback()
            logger_exception()

    @staticmethod
    def convert_keys(keys):
        keys = [f'`{_k}`' for _k in keys]
        return ', '.join(keys)

    @staticmethod
    def convert_insert_data(value_list, placeholder='%s'):
        if not value_list:
            return [], [], []
        keys = tuple(value_list[0].keys())
        place = tuple([placeholder] * len(keys))
        values = []
        for item in value_list:
            value = list()
            for k in keys:
                if k is None:
                    value.append(None)
                else:
                    value.append(f'`{item[k]}`')
            values.append(tuple(value))
        return keys, ', '.join(place), values

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
                    where_keys.append(f'`{_k}` {_join} %s')
                    where_vals.append(_v)
                    keys.append(_k)
            else:
                where_keys.append(f'`{_k}` {_join} %s')
                where_vals.append(_v)
                keys.append(_k)
        place = _and.join(where_keys)
        values = tuple(where_vals)
        return keys, place, values


class SqlAlchemyUtil(SqlUtil):

    def __init__(self, host, port, user, password, database, charset='utf-8'):
        super().__init__(host, port, user, password, database, charset)
        self.cursor = None
        uri = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
        engine = create_engine(uri)
        # 通过sessionmaker方法创建了一个Session工厂
        self.Session = sessionmaker(bind=engine)

    def connection(self):
        # 通过调用工厂方法来创建一个Session对象
        session = self.Session()
        return session, session

    def mogrify(self, sql, data=None):
        if not self.cursor:
            connect = pymysql.connect(**self.config)
            self.cursor = connect.cursor(pymysql.cursors.DictCursor)
        return self.cursor.mogrify(sql, data)

    def command(self, sql, data=None, calc_rows=False):
        connect, cursor = self.connection()
        results = []
        row_count = 0
        trans_opt = self.trans_opt(sql)
        try:
            if sql.split(' ')[0].upper() == 'INSERT':
                Logger.debug(sql)
                result = cursor.execute(sql, data)
            else:
                sql = self.mogrify(sql, data)
                Logger.debug(sql)
                result = cursor.execute(sql)
            if hasattr(result, 'rowcount'):
                row_count = result.rowcount
            if not trans_opt:
                results = [dict(item.items()) for item in result]

            if calc_rows:
                result = cursor.execute("SELECT FOUND_ROWS() as total")
                rows = [dict(zip(item.keys(), item)) for item in result]
                row_count = rows[0].get('total', 0)

            if trans_opt:
                connect.commit()
        except:
            if trans_opt:
                connect.rollback()
            logger_exception()
        finally:
            connect.close()
        if calc_rows:
            return results, row_count
        return row_count if trans_opt else results

    def insert(self, table, value_list):
        if not value_list:
            return 0
        value_list = value_list if isinstance(value_list, list) else value_list
        keys, place, values = self.convert_insert_data(value_list, placeholder="?")
        sql = SqlUtil.INSERT_TABLE.format(table=table, keys=self.convert_keys(keys),
                                          values=', '.join([f':{key}' for key in keys]))
        return self.command(sql, data=value_list)


class DBPoolUtil(SqlUtil):

    def __init__(self, host, port, user, password, database, charset='utf-8', shareable=False):
        super().__init__(host, port, user, password, database, charset)
        if not shareable:
            self.pool_conn = PersistentDB(
                creator=pymysql,  # 使用链接数据库的模块
                maxusage=None,    # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],    # 开始会话前执行的命令列表。
                ping=1,           # ping MySQL服务端，检查是否服务可用。
                closeable=False,  # 如果为False时， conn.close() 实际上被忽略，供下次使用，再线程关闭时，才会自动关闭链接。如果为True时， conn.close()则关闭链接，那么再次调用pool.connection时就会报错，因为已经真的关闭了连接（pool.steady_connection()可以获取一个新的链接）
                threadlocal=None, # 本线程独享值得对象，用于保存链接对象，如果链接对象被重置
                **self.config
            )
        else:
            self.pool_conn = PooledDB(
                creator=pymysql,   # 使用链接数据库的模块
                maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=2,       # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=5,       # 链接池中最多闲置的链接，0和None不限制
                maxshared=3,       # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
                blocking=True,     # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,     # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],     # 开始会话前执行的命令列表。
                ping=0,            # ping MySQL服务端，检查是否服务可用。
                **self.config
            )

    def connection(self):
        connect = self.pool_conn.connection(shareable=False)
        cursor = connect.cursor(pymysql.cursors.DictCursor)
        return connect, cursor