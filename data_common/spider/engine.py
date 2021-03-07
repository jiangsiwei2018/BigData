# encoding=utf-8
import os
from data_common.spider.scheduler import Scheduler

def read_urls(file_path):
    with open(file_path, 'r+', encoding='utf-8') as fp:
        lines = fp.readlines()
        return [line.strip() for line in lines if line.strip()]


def engine():
    path = os.path.dirname(__file__) + '/urls.txt'
    urls = read_urls(path)
    htmls = Scheduler.download(urls)
    data = Scheduler.analysis(htmls)
    Scheduler.storage(data)


if __name__ == '__main__':
    engine()