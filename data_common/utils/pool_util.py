# coding=utf-8

from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool 


class PoolUtility:

    min_thread_num = 1
    max_thread_num = 8
    min_process_num = 1
    max_process_num = 8

    @staticmethod
    def thread_pool(fun, args, thread_num=0):
        if thread_num:
            pool = ThreadPool(thread_num)
        else:
            pool = ThreadPool(PoolUtility.max_thread_num)
        results = pool.map(fun, args)
        pool.close()
        pool.join()
        return results

    @staticmethod
    def process_pool(fun, args, process_num=0):
        if process_num:
            pool = ProcessPool(process_num)
        else:
            pool = ProcessPool(PoolUtility.max_process_num)
        results = pool.map(fun, args)
        pool.close()
        pool.join()
        return results

    @staticmethod
    def process_pool_iter(fun, iter_args, process_num=0):
        if process_num:
            pool = ProcessPool(process_num)
        else:
            pool = ProcessPool(PoolUtility.max_process_num)
        results = pool.imap(fun, iter_args)
        pool.close()
        pool.join()
        return results
