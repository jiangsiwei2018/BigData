# coding=utf-8
# from bigdata.dao.db_mysql_util import SqlUtil
from data_common.dao.mysql_util import SqlAlchemyUtil as SqlUtil
# from bigdata.dao.db_mysql_util import DBPoolUtil as SqlUtil


if __name__ == '__main__':
    table = 'user'
    sql_util = SqlUtil('127.0.0.1', 3306, 'root', '123456', 'bigdata')

    table_str = "`id` char(64) DEFAULT NULL,\
                 `name` varchar(500) DEFAULT NULL,\
                 `age` varchar(500) DEFAULT NULL"
    create_table_sql = SqlUtil.CREATE_TABLE.format(table=table,
                                                   keys=table_str,
                                                   index='id')
    # print(sql_util.command(f'DROP TABLE {table}'))
    if not sql_util.is_exists_table(table):
        sql_util.command(create_table_sql)
    import time
    where = {'age': {'$ge': 20}, 'name':'Tom'}
    update = {'age': 21}

    data = [
        {'name': 'Tom', 'age': 20, 'id': f'1{time.time()*1000}'},
        {'name': 'Jack', 'age': 21, 'id': f'2{time.time()*1000}'},
        {'name': 'Jim', 'age': 22, 'id': f'3{time.time()*1000}'}
    ]
    print(sql_util.insert(table, data))
    print(sql_util.command(f'select * from {table}'))
    print(sql_util.find(table, where={'name': 'Tom'}, keys=['id', 'name'],  multi=True, calc_rows=True))
    print(sql_util.update(table, update, where))
    print(sql_util.exists(table, 4))
    print(sql_util.delete(table, {'name': 'Jack'}))