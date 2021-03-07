# coding=utf8
import re

import lxml
from lxml import etree
from data_common.utils.common import Common


class XPathUtil:

    html_node_cache = {}

    @staticmethod
    def get_root(html):
        if isinstance(html, str) or isinstance(html, bytes):
            _id = Common.get_md5(html)
            if _id not in XPathUtil.html_node_cache:
                XPathUtil.html_node_cache[_id] = etree.HTML(html)
            return XPathUtil.html_node_cache[_id]
        return html

    @staticmethod
    def get_roots(root, xpath):
        if isinstance(root, lxml.etree._Element):
            html = XPathUtil.get_raw_html(root)
            root = XPathUtil.get_root(html)
        return root.xpath(xpath)

    @staticmethod
    def get_list(root, xpath):
        xpath_items = XPathUtil.get_roots(root, xpath)
        items = []
        for item in xpath_items:
            if isinstance(item, lxml.etree._Element):
                items.append(XPathUtil.get_node_text(item))
            elif isinstance(item, lxml.etree._ElementUnicodeResult):
                items.append(item.strip())
        return items

    @staticmethod
    def get_string(root, xpath, join_split=' '):
        xpath_items = XPathUtil.get_list(root, xpath)
        return join_split.join(xpath_items)

    @staticmethod
    def get_raw_html(node):
        return str(etree.tostring(node), encoding='utf-8')

    @staticmethod
    def get_node_text(element_node):
        text = element_node.xpath('string(.)')
        text = Common.get_filter_text(text)
        return text