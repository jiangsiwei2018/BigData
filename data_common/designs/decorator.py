# coding=utf-8
import time
from functools import wraps
import traceback


def stat_time(func):
    """统计函数或方法运行的时间"""
    @wraps(func)
    def opt(*arg, **kwargs):
        start_time = time.time()
        func(*arg, **kwargs)
        end_time = time.time()
        cha_time = end_time - start_time
        print(f'{func.__name__} method spend time {round(cha_time, 3)}')
    return opt


def retry(max_times=3):
    def retry_func(func):
        @wraps(func)
        def wrapper(*arg, **kwargs):
            res = None
            for i in range(max_times):
                try:
                    res = func(*arg, **kwargs)
                    break
                except:
                    print(traceback.print_exc())
            return res
        return wrapper
    return retry_func


if __name__ == '__main__':

    @retry(3)
    def abc():
        return 3 / 0

    abc()
