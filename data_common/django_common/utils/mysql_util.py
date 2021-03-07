# coding=utf-8
from data_common.dao.mysql_util import SqlUtil
from data_common.utils.log_util import Logger, logger_exception
from django.db import connections


class DjangoSqlUtil(SqlUtil):

    def __init__(self, app_label='default'):
        self.app_label = app_label

    def connection(self):
        cursor = connections[self.app_label].cursor()
        return cursor, cursor

    def command(self, sql, data=None, calc_rows=False):
        connect, cursor = self.connection()
        data_list = []
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
            if not trans_opt:
                results = cursor.fetchall()
                keys = [col[0] for col in cursor.description]
                for result in results:
                    result = dict(zip(keys, list(result)))
                    data_list.append(result)
            if calc_rows:
                cursor.execute("SELECT FOUND_ROWS() as total")
                rows = cursor.fetchall()
                row_count = list(rows)[0][0]
        except:
            logger_exception()
        finally:
            cursor.close()
            connect.close()
        if calc_rows:
            return data_list, row_count
        return row_count if trans_opt else data_list
