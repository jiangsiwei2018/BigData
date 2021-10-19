# coding=utf-8

class SingletonTypeD(type):
    """
    最优先使用的方式, 此种方法定义的单实例可以被继承
    1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
    2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
    """
    def __call__(cls, *args, **kwargs):
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(cls.__name__, args, temp)
        if not hasattr(cls, "_instance_pool"):
            cls._instance_pool = dict()
        if cls_key not in cls._instance_pool:
            cls_instance = super().__call__(*args, **kwargs)
            cls._instance_pool[cls_key] = cls_instance
        return cls._instance_pool[cls_key]


class SingletonTypeL(type):
    """
    和SingletonType一样, 此种方法定义的单实例的类【可以被继承】
    1.类由type创建，创建类时，type的__init__方法自动执行，类() 执行type的 __call__方法(类的__new__方法,类的__init__方法)
    2.对象由类创建，创建对象时，类的__init__方法自动执行，对象()执行类的 __call__ 方法
    """
    def __call__(cls, *args, **kwargs):
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(cls.__name__, args, temp)
        if not hasattr(cls, "_instance_pool"):
            cls._instance_pool = list()
        for cls_key_temp, _instance in cls._instance_pool:
            if cls_key_temp == cls_key:
                return _instance
        else:
            _instance = super().__call__(*args, **kwargs)
            cls._instance_pool.append((cls_key, _instance))
            return _instance


class SingletonDecC(object):
    """
    装饰器类
    函数作为装饰器返回的是一个函数，函数被调用过程中实际上是间接地  调用其内部包裹的被装饰的对象。
    类作为装饰器要想达到相同的效果只需要将类的对象返回，并且其对象是可以调用的。这是上面这个例子表达的一个核心思想。
    其思想基本上就是对被包裹对象的调用实际上调用的是类对象的__call__函数，该函数实际上是对被装饰对象的一次封装。
    """

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(self.cls.__name__, args, temp)
        if not hasattr(self.cls, "_instance_pool"):
            self.cls._instance_pool = dict()
        if cls_key not in self.cls._instance_pool:
            self.cls._instance_pool[cls_key] = self.cls(*args, **kwargs)
        return self.cls._instance_pool[cls_key]

    def __getattr__(self, key):
        return getattr(self.cls, key, None)


def SingletonDecM(cls):
    """装饰器方法"""
    _instance_pool = {}
    def _singleton(*args, **kwargs):
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(cls.__name__, args, temp)
        if cls_key not in _instance_pool:
            _instance_pool[cls_key] = cls(*args, **kwargs)
        return _instance_pool[cls_key]
    return _singleton


class SingletonClass(object):
    """使用继承方式"""

    @staticmethod
    def get_instance(cls, *args, **kwargs):
        """
        单实例原始方法1
        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(cls.__name__, args, temp)
        if not hasattr(cls, "_instance_pool"):
            cls._instance_pool = dict()
        if cls_key not in cls._instance_pool:
            cls._instance_pool[cls_key] = cls(*args, **kwargs)
        return cls._instance_pool[cls_key]

    def __new__(cls, *args, **kwargs):
        """
        单实例原始方法1, 【有缺陷！！！】
        此种方式 new对象之后，还是要__init__, 也就是说参数还是会被初始化
        此种方式 做单实例时，需满足 初始参数不被初始化 的场景
        :param args:
        :param kwargs:
        :return:
        """
        temp = list(sorted(kwargs.items(), key=lambda x: x[0]))
        cls_key = '{}_{}_{}'.format(cls.__name__, args, temp)
        if not hasattr(cls, "_instance_pool"):
            cls._instance_pool = dict()
        if cls_key not in cls._instance_pool:
            cls._instance_pool[cls_key] = object.__new__(cls)
        return cls._instance_pool[cls_key]


if __name__ == '__main__':
    # example

    @SingletonDecM
    class A1:

        def __init__(self, a, b, **kwargs):
            print('__init__ {} {}'.format(a, b))
            self.a1 = a
            self.a2 = b
            self.a3 = kwargs.get('c', None)
            # print(self.a1, self.a2)

        def set_a(self, a):
            self.a1 = self.a1 + a

        def set_b(self, b):
            self.a2 = b


    d = {'c': 5, 'd': 6}
    c = A1(1, 1, **d)
    print(c.a1)
    c.set_a(1)
    print(c.a1)

    d = {'d': 6, 'c': 5}
    c2 = A1(1, 1, **d)
    print(c2.a1)
    c3 = A1(4, 1, **d)
    print(c3.a1)

    print(id(c), id(c2), id(c3))



