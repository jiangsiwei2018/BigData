# coding=utf-8

# 比较重要的几点：
# 1. 首次设置，后续设置不生效，可以针对多线程/多进程/分布式进行处理
# 2. redis shading + hash 一致性组成组分布式
# 3. 关于设置过期问题，能够有保证 数据有效性
import json

import redis
from data_common.designs.singleton import SingletonType


class RedisUtil(metaclass=SingletonType):

    def __init__(self, host, port=6379, password=None):
        self.client = redis.Redis(host=host, port=port, password=password)

    def command(self, *args, **kwargs):
        return self.client.execute_command(*args, **kwargs)

    def get(self, key):
        value = self.command('GET', key)
        if str(value).startswith('{') and str(value).endswith('}'):
            value = json.dump(value)
        return value

    def set(self, key, value, *args, **kwargs):
        """
        ex，过期时间（秒）
     　　px，过期时间（毫秒）
     　　nx，如果设置为True，则只有name不存在时，当前set操作才执行
     　　xx，如果设置为True，则只有name存在时，岗前set操作才执行
        """
        if isinstance(value, list) or isinstance(value, dict):
            value = json.dump(value)
        return self.command('SET', key, value, *args, **kwargs)

    def hget(self, name, key):
        value = self.command('HGET', name, key)
        if str(value).startswith('{') and str(value).endswith('}'):
            value = json.dump(value)
        return value

    def hset(self, name, key, value, *args, **kwargs):
        """
        ex，过期时间（秒）
     　　px，过期时间（毫秒）
     　　nx，如果设置为True，则只有name不存在时，当前set操作才执行
     　　xx，如果设置为True，则只有name存在时，岗前set操作才执行
        """
        if str(value).startswith('{') and str(value).endswith('}'):
            value = json.dump(value)
        return self.command('HSET', name, key, value, *args, **kwargs)

    # mget()
    # mset()
    # mhset()
    # mhset()


class RedisPoolUtil(RedisUtil):

    def __init__(self, host, port=6379, password=None, max_connections=1024):
        pool = redis.ConnectionPool(host=host, port=port,
                                    password=password, max_connections=max_connections)
        self.client = redis.Redis(connection_pool=pool)


# set(name, value, ex=None, px=None, nx=False, xx=False)
# 　　在Redis中设置值，默认，不存在则创建，存在则修改
# 　　参数：
# 　　ex，过期时间（秒）
# 　　px，过期时间（毫秒）
# 　　nx，如果设置为True，则只有name不存在时，当前set操作才执行
# 　　xx，如果设置为True，则只有name存在时，岗前set操作才执行
#
# setnx(name, value)
# # 设置值，只有name不存在时，执行设置操作（添加）
#
# setex(name, value, time)　　  # 设置值
# 　　  # 参数：
# # time，过期时间（数字秒 或 timedelta对象）
# psetex(name, time_ms, value)　　  # 设置值
# 　　  # 参数：　　　　# time_ms，过期时间（数字毫秒 或 timedelta对象）
#
# mset(*args, **kwargs)
# 批量设置值
# 　　如：
# mset(k1='v1', k2='v2')
# 或
# mget({'k1': 'v1', 'k2': 'v2'})
#
# get(name)
# 获取值
#
# mget(keys, *args)
# 批量获取
# 　　 如：
# mget('name', 'root')
# 或
# r.mget(['name', 'root'])
#
# getset(name, value)
# 设置新值并获取原来的值
#
# getrange(key, start, end)
# # 获取子序列（根据字节获取，非字符）
# 　　  # 参数：
# # name，Redis 的 name
# # start，起始位置（字节）
# # end，结束位置（字节）
# 　　  # 如： "你好" ，0-3表示 "你"   (utf8中一个中文字符占三个字节)
#
# setrange(name, offset, value)
# # 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加）
# 　　  # 参数：
# # offset，字符串的索引，字节（一个汉字三个字节）
# # value，要设置的值
#
