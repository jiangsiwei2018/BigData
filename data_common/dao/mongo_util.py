# encoding=utf-8
import pymongo
from data_common.utils.log_util import Logger, logger_exception
from data_common.designs.decorator import retry


class MongodbUtil:

    def __init__(self, host, port, database, username=None, password=None):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self._client = None
        self.connection()

    @retry(3)
    def connection(self):
        self._client = pymongo.MongoClient(self.host, self.port)
        return True

    @retry(3)
    def check(self):
        try:
            self._client.admin.command('ping')
            return True
        except:
            logger_exception()
            Logger.error('Server not available!')
            return self.connection()

    def command(self, database, collection, opt, *args, **kwargs):
        if not self.check():
            Logger.error('MongoDB connect failed!')
            return
        opt = getattr(self._client[database][collection], opt, None)
        if opt:
            Logger.debug(f'{database}\t{collection}\t{opt}\t{args}\t{kwargs}')
            return opt(*args, **kwargs)

    def insert(self, coll, rows, database=None):
        database = database if database else self.database
        return self.command(database, coll, 'insert', rows)

    def find(self, coll, where, database=None):
        database = database if database else self.database
        return self.command(database, coll, 'find', filter=where)

    def count(self, coll, where, database=None):
        database = database if database else self.database
        return self.command(database, coll, 'find', filter=where).count()

    def update(self, coll, update, where, database=None):
        database = database if database else self.database

        return self.command(database, coll, 'update_many', filter=where, update={'$set': update})

    def delete(self, coll, where, database=None):
        database = database if database else self.database
        return self.command(database, coll, 'delete_many', filter=where)