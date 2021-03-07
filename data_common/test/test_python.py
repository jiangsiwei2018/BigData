# coding=utf-8
class T:
    num = 0

    def __init__(self):
        self.name = 'aaa'

    @classmethod
    def add(cls, num):
        cls.num += num

    @classmethod
    def add_name(cls, s):
        cls.name += s


if __name__ == '__main__':
    T.add(4)
    print(T.num)

    t = T()
    T.add(5)
    print(t.num)