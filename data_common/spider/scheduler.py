# encoding=utf-8
from data_common.spider.downloader import Download
from data_common.spider.analysis import Analysis
from data_common.spider.storage import Storage

class Scheduler:

    def __init__(self):
        pass

    @staticmethod
    def download(urls):
        urls = urls if isinstance(urls, list) else [urls]
        htmls = []
        # 下载
        for url in urls:
            htmls.append((url, Download.get(url)))
        return htmls

    @staticmethod
    def analysis(_tuple):
        """[(url, html), (url, html)]"""
        #  解析
        data = []
        for url, html in _tuple:
            data.append(Analysis.parse(url, html))
        return data

    @staticmethod
    def storage(data):
        # 存储
        for params in data:
            Storage.storage(params)
