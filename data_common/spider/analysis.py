# encoding=utf-8
from lxml import etree

class Analysis:

    def __init__(self):
        pass

    @staticmethod
    def parse(url, html):
        title = Util.get_text(html, '//*[@id="cb_post_title_url"]')
        title = title[0].text
        body_list = Util.get_text(html, '//*[@id="cnblogs_post_body"]//p')
        body = [item.text for item in body_list]
        params = {
            'title': title,
            'body': body,
            'url': url
        }
        return params


class Util:

    @staticmethod
    def get_text(html, xpath):
        root = etree.HTML(html)
        return root.xpath(xpath)