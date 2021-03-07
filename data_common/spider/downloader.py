# encoding=utf-8
import requests


class Download:

    """
    1. 高效爬取
    2. 常见反反爬虫手段
    3. 数据量的问题：并发, 分布式
    """

    def __init__(self):
        pass

    @staticmethod
    def get(url, headers={}):
        html = requests.get(url, headers=headers)
        return html.text

    @staticmethod
    def post(url, data={}, headers={}):
        html = requests.post(url, data=data, headers=headers)
        return html.text

    @staticmethod
    def get_headers(params):
        """..."""
        return params