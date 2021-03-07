# coding=utf-8
from functools import wraps


class Singleton:

    instance_pool = {}
    instance_pool_list = []


class SingletonType(type):
    """
    最优先使用的方式, 此种方法定义的单实例可以被继承
    1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
    2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
    """
    def __call__(cls, *args, **kwargs):
        cls_key = (cls.__name__, args, tuple(kwargs.items()))
        cls_instance = Singleton.instance_pool.get(cls_key, None)
        if not cls_instance:
            cls_instance = super(SingletonType, cls).__call__(*args, **kwargs)
            Singleton.instance_pool[cls_key] = cls_instance
        return cls_instance


class SingletonListType(type):
    """
    和SingletonType一样, 此种方法定义的单实例的类【可以被继承】
    1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
    2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
    """
    def __call__(cls, *args, **kwargs):
        for _cls_name, _args, _kwargs, _instance in Singleton.instance_pool_list:
            if (_cls_name, _args, _kwargs) == (cls.__name__, args, kwargs):
                return _instance
        else:
            _instance = super(SingletonListType, cls).__call__(*args, **kwargs)
            Singleton.instance_pool_list.append((cls.__name__, args, kwargs, _instance))
            return _instance


class SingletonDecClass:
    """
    使用装饰器方法，但此种方法定义的单实例的类【不可以被继承】
    1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
    2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
    """
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        for _cls_name, _args, _kwargs, _instance in Singleton.instance_pool_list:
            if (_cls_name, _args, _kwargs) == (self.cls.__name__, args, kwargs):
                return _instance
        else:
            _instance = self.cls(*args, **kwargs)
            Singleton.instance_pool_list.append((self.cls.__name__, args, kwargs, _instance))
            return _instance


class SingletonDecMethod(object):
    """
    使用装饰器方法，但此种方法定义的单实例的类【不可以被继承】
    """

    @staticmethod
    def singleton(cls):
        # 定义一个私有方法,wraps作用不知道的自己查,不感兴趣的也不用知道
        @wraps(cls)
        def __wrapper(*args, **kwargs):
            cls_key = (cls.__name__, args, kwargs)
            cls_instance = Singleton.instance_pool.get(cls_key)
            if not cls_instance:
                cls_instance = cls(*args, **kwargs)
                cls._instance_pool[cls_key] = cls_instance
            return cls_instance
        return __wrapper


class SingletonExample(object):
    """
    使用 __new__ 定义单实例
    正常定义类的模式, 需要重写 __new__方法
    """
    _instance = None

    def __init__(self, *args, **kwargs):
        pass

    def function(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not SingletonExample._instance:
            SingletonExample._instance = object.__new__(cls, *args, **kwargs)
        return SingletonExample._instance


if __name__ == '__main__':
    # example
    @SingletonDecorator
    class A1:

        def __init__(self, a=1, b=1):
            self.a1 = a
            self.a2 = b

        def set_a(self, a):
            self.a1 = self.a1 + a

        def set_b(self, b):
            self.a2 = b


    # class A2(A1):
    #
    #     def __init__(self, a=0, b=3):
    #         super(A2, self).__init__(a, b)
    #
    #     def set_a(self, a):
    #         self.a1 = a + 2

    c = A1(1, 1)

    print(c.a1)
    c.set_a(1)
    print(c.a1)

    print(A1(1, 1).a1)
    #
    # c2 = A2(2, 2)
    # c2.set_a(2)
    # print(A2(10, 2).a1)
    # print(A2(2, 2).a1)
