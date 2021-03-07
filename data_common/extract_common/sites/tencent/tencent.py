# coding=utf-8
from data_common.extract_common.sites.site_base import BaseSite


class QQ(BaseSite):

    url_patterns = ['https?://www.qq.com']

    def __init__(self):
        pass

    def process(self):
        pass

