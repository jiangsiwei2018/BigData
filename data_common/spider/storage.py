# encoding=utf-8
import hashlib
from data_common.spider.sqldao import SqlUtil

class Storage:

    table = 'spider'

    def __init__(self):
        pass

    @staticmethod
    def storage(params):
        """
        insert or update params
        :param params:
        :return:
        """
        sql_util = SqlUtil('127.0.0.1', 3306, 'root', '123456', 'mysql')
        _id = Storage.url2md5(url=params['url'])
        if sql_util.exists(Storage.table, _id):
            sql_util.update(Storage.table, where={'id': _id}, dict_value=params)
        else:
            sql_util.insert(Storage.table, params)

    @staticmethod
    def url2md5(url):
        if isinstance(url, str):
            url = url.encode('utf-8')
        m2 = hashlib.md5()
        m2.update(url)
        return m2.hexdigest()

