# coding=utf-8
import functools


class Lazy:
    """
    延迟模式：在第一次使用时才会去初始化，这样就可以达到减少消耗的目的
    """

    def __init__(self, fun):
        self.fun = fun
        functools.update_wrapper(self, fun)

    def __get__(self, obj, _type):
        if obj is None:
            return self
        val = self.fun(obj)
        # 等同 obj.__dict__[self.fun.__name__] = val
        setattr(obj, self.fun.__name__, val)
        return val


def lazy(fn):
    attr = '_lazy__' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr):
            setattr(self, attr, fn(self))
        return getattr(self, attr)

    return _lazy_property


class Person:
    def __init__(self):
        self.call_count2 = 0

    @Lazy
    def relatives(self):
        # Get all relatives, let's assume that it costs much time.
        relatives = "Many relatives."
        print(relatives)
        return relatives

    @lazy
    def parents(self):
        self.call_count2 += 1
        print(self.call_count2)
        return "Father and mother"


if __name__ == '__main__':
    person = Person()
    person.relatives
    person.relatives
    person.parents
    person.parents