# -*- coding:utf-8 -*-
import sys
import time


class ProgressBar:

    @staticmethod
    def progress_test():
        bar_length = 100
        for percent in range(0, 101):
            hashes = '#' * int(percent / 100.0 * bar_length)
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rPercent: [%s] %d%%" % (hashes + spaces, percent))
            sys.stdout.flush()
            time.sleep(0.05)

    class ProgressBar1:
        def __init__(self, width=50):
            self.pointer = 0
            self.width = width

        def __call__(self, x):
            # print('\t')
            self.pointer = int(self.width * (x / 100.0))
            return "|" + "#" * self.pointer + "-" * (self.width - self.pointer) + "| %d %% done" % int(x)

    class ProgressBar2:
        def __init__(self, width=50):
            self.pointer = 0
            self.width = width

        def __call__(self,x):
            # print('\r')
            self.pointer = x
            return "|" + "#" * self.pointer + "-" * (100 - self.pointer)+ "| %d %% done" % int(x)

    @staticmethod
    def run():
        # progress_test()
        ProgressBar.progress_test()
        # pb = ProgressBar.ProgressBar1()
        # for i in range(101):
        #     # os.system('cls')
        #     print(pb(i))
        #     time.sleep(0.02)
        #
        # pb = ProgressBar.ProgressBar2()
        # for i in range(101):
        #     # os.system('cls')
        #     print(pb(i))
        #     time.sleep(0.02)


if __name__ == '__main__':
    ProgressBar.run()