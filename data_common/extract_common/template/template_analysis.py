# encoding=utf-8
import inspect
import re

from data_common.utils.xpath_util import XPathUtil
from data_common.extract_common.template import template_methods
from data_common.designs.factory import FactoryClass
from data_common.extract_common.template.template_manager import TemplateManager


class TemplateAnalysis:

    def __init__(self, template_file=None, methods_file=None):
        self.template_file = template_file
        self.methods_file = methods_file
        self.methods_class = self.import_methods()

    def import_methods(self):
        prefix = FactoryClass.get_module_prefix(template_methods)
        module = FactoryClass.import_module(self.methods_file, prefix)
        for name, _class in FactoryClass.get_module_members(module).items():
            if inspect.isclass(_class) and issubclass(_class, template_methods.TemplateMethods):
                return _class

    def process(self, url, html):
        template = TemplateManager(self.template_file).get_template(url)
        params = self.process_node(html, template['template'])
        params['url'] = url
        return params

    def process_node(self, html, template):
        params = dict()
        root = XPathUtil.get_root(html)
        for current in template:
            if 'current' in current and 'children' in current:
                _current = current['current']
                children_template = current['children']
                mode = current.get("mode", "parallel-xpath")
                if mode == 'parallel-tree':
                    # mode="tree"仅限子节点
                    nodes = Tree.create_tree(root, _current['xpath'])
                    children_list = AnalysisTree(nodes, children_template).get_value()
                    params[_current['key']] = children_list
                else:
                    # 进行不断循环
                    if mode == 'parallel-split':
                        roots = self.process_parallel(root, children_template)
                    else:
                        roots = XPathUtil.get_roots(root, _current['xpath'])
                    children_list = []
                    for _root in roots:
                        _dict = self.process_node(_root, children_template)
                        children_list.append(_dict)
                    params[_current['key']] = children_list
            else:
                _current = current['current'] if 'current' in current else current
                key = _current.get('key')
                xpath = _current.get('xpath')
                method = _current.get('method')
                _type = _current.get('type', 'text')
                if _type == 'text':
                    value = XPathUtil.get_string(root, xpath)
                else:
                    value = XPathUtil.get_list(root, xpath)
                params[key] = self.process_fun(method, value, node=root, template=_current)
        return params

    def process_fun(self, method_name, value, *args, **kwargs):
        if not method_name:
            return value
        func = getattr(self.methods_class, method_name, None)
        if func and inspect.isfunction(func):
            return func(value, *args, **kwargs)
        else:
            return value

    @staticmethod
    def is_block_start(node, node_string, block_start):
        """
        :param reg:
        :param node: 节点的字符串
        :return:
        """
        reg = block_start.get('reg')
        tag = block_start.get('tag')
        _class = block_start.get('class')
        if reg and re.search(reg, node_string):
            return True
        if tag and not _class:
            if node.tag == tag:
                return True
        if tag and _class:
            if node.tag == tag and _class in tag.attrib.get('class', ''):
                return True
        return False

    def process_parallel(self, root, current):
        """
        另外获取kv对的roots思路：通过获取所有子节点路径，扁平所有xpath，然后进行统计；
        频率出现较高的且成对出现的，可能是kv取值区域(其实是一种聚类的形式)
        :param root:
        :param current:
        :return:
        """
        index = 0
        block_nodes_map = {}
        block_start = current.get("block_start", {})
        _current = current['current']
        roots = XPathUtil.get_roots(root, _current['xpath'])
        for node in roots:
            node_string = XPathUtil.get_raw_html(node)
            if self.is_block_start(node, node_string, block_start):
                if index not in block_nodes_map:
                    block_nodes_map[index] = []
            if block_nodes_map.get(index):
                continue
            block_nodes_map[index].append(node)
        # 重新组装成nodes
        block_nodes_list = []
        for index, _nodes in block_nodes_map.items():
            block = f'<div class="block">{"".join(_nodes)}</div>'
            block_nodes_list.append(block)
        return block_nodes_list


class Tree:

    class TreeNode:
        def __init__(self):
            self.children = []
            self.attrib = None
            self.tag = None
            self.text = None
            self.xpath = None

        def get_dict(self):
            return self.__dict__

    @staticmethod
    def get_nodes(nodes):
        tree_nodes = []
        for node in nodes:
            tree_node = Tree.TreeNode()
            tree_node.tag = node.tag
            tree_node.attrib = node.attrib
            tree_node.text = XPathUtil.get_node_text(node)
            children_nodes = node.getchildren()
            if children_nodes:
                tree_node.children = Tree.get_nodes(children_nodes)
            tree_nodes.append(tree_node)
        return tree_nodes

    @staticmethod
    def create_tree(html, xpath):
        if isinstance(html, str):
            root = XPathUtil.get_root(html)
        else:
            root = html
        nodes = XPathUtil.get_roots(root, xpath)
        tree_nodes = Tree.get_nodes(nodes)
        return tree_nodes


class AnalysisTree:

    def __init__(self, tree_nodes, templates):
        self.value_list = []
        self.templates = templates
        self.tree_nodes = tree_nodes

    def get_value(self):
        self.get_parallel(self.tree_nodes)
        return self.value_list

    def get_parallel(self, tree_nodes):
        for tree_node in tree_nodes:
            values = {}
            for node in tree_node.children:
                for template in self.templates:
                    k, child = template['key'], template.get("child")
                    if self.pos_flag(node, template):
                        if k not in values:
                            values[k] = []
                        if child:
                            for node_child in node.children:
                                values[k].append(node_child.text)
                        else:
                            values[k].append(node.text)
            if values:
                self.value_list.append(values)
            self.get_parallel(tree_node.children)

    @staticmethod
    def pos_flag(node, template):
        k, tag, attrib, attrib_mode = \
            template['key'], template['tag'], template.get('attrib', {}), template.get('attrib_mode', 'equal')
        flag = False
        if tag == node.tag:
            for _t, _v in attrib.items():
                if attrib_mode == 'equal' and node.attrib.get(_t, '') == _v:
                    flag = True
                elif attrib_mode == 'reg' and re.search(_v, node.attrib.get(_t, '')):
                    flag = True
            if not attrib:
                flag = True
        return flag

if __name__ == '__main__':
    import os
    # path = os.path.dirname(__file__) + '/template_methods.py'
    # module = TemplateAnalysis(methods_file=path)
    # print(module.methods_class)
    # process_text = getattr(module.methods_class, 'process_text')
    #
    # print(inspect.isfunction(process_text))



    # html = '<div id="info">\n        <span><span class="pl">导演</span>: <span class="attrs"><a href="/celebrity/1022652/" rel="v:directedBy">格蕾塔·葛韦格</a></span></span><br>\n        <span><span class="pl">编剧</span>: <span class="attrs"><a href="/celebrity/1022652/">格蕾塔·葛韦格</a> / <a href="/celebrity/1037345/">路易莎·梅·奥尔科特</a></span></span><br>\n        <span class="actor"><span class="pl">主演</span>: <span class="attrs"><span><a href="/celebrity/1022004/" rel="v:starring">西尔莎·罗南</a> / </span><span><a href="/celebrity/1053624/" rel="v:starring">艾玛·沃森</a> / </span><span><a href="/celebrity/1378921/" rel="v:starring">弗洛伦丝·皮尤</a> / </span><span><a href="/celebrity/1395069/" rel="v:starring">伊莱扎·斯坎伦</a> / </span><span><a href="/celebrity/1006983/" rel="v:starring">劳拉·邓恩</a> / </span><span style="display: inline;"><a href="/celebrity/1325862/" rel="v:starring">蒂莫西·柴勒梅德</a> / </span><span style="display: inline;"><a href="/celebrity/1054437/" rel="v:starring">梅丽尔·斯特里普</a> / </span><span style="display: inline;"><a href="/celebrity/1027856/" rel="v:starring">鲍勃·奥登科克</a> / </span><span style="display: inline;"><a href="/celebrity/1326707/" rel="v:starring">詹姆斯·诺顿</a> / </span><span style="display: inline;"><a href="/celebrity/1018067/" rel="v:starring">路易·加瑞尔</a> / </span><span style="display: inline;"><a href="/celebrity/1009288/" rel="v:starring">克里斯·库珀</a> / </span><span style="display: inline;"><a href="/celebrity/1009889/" rel="v:starring">崔西·莱茨</a> / </span><span style="display: inline;"><a href="/celebrity/1386474/" rel="v:starring">艾比·奎因</a> / </span><span style="display: inline;"><a href="/celebrity/1366443/" rel="v:starring">萨沙·弗若洛娃</a> / </span><span style="display: inline;"><a href="/celebrity/1351693/" rel="v:starring">莉莉·恩格勒特</a> / </span><span style="display: inline;"><a href="/celebrity/1082829/" rel="v:starring">爱德华德·弗莱彻</a> / </span><span style="display: inline;"><a href="/celebrity/1386049/" rel="v:starring">杰妮·霍蒂谢尔</a> / </span><span style="display: inline;"><a href="/celebrity/1411091/" rel="v:starring">多梅尼克·阿尔迪诺</a> / </span><span style="display: inline;"><a href="/celebrity/1251841/" rel="v:starring">汤姆·斯特拉特福</a> / </span><span style="display: inline;"><a href="/celebrity/1035084/" rel="v:starring">托马斯·马里亚诺</a> / </span><span style="display: inline;"><a href="/celebrity/1421394/" rel="v:starring">哈德莉·罗宾逊</a> / </span><span style="display: inline;"><a href="/celebrity/1421395/" rel="v:starring">杰米·加扎里安</a></span><a href="javascript:;" class="more-actor" title="更多主演" style="display: none;">更多...</a></span></span><br>\n        <span class="pl">类型:</span> <span property="v:genre">剧情</span> / <span property="v:genre">爱情</span><br>\n        <span class="pl">官方网站:</span> <a href="http://www.littlewomen.movie/" rel="nofollow" target="_blank">www.littlewomen.movie/</a><br>\n        <span class="pl">制片国家/地区:</span> 美国<br>\n        <span class="pl">语言:</span> 英语<br>\n        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2020-08-25(中国大陆)">2020-08-25(中国大陆)</span> / <span property="v:initialReleaseDate" content="2019-12-25(美国)">2019-12-25(美国)</span><br>\n        <span class="pl">片长:</span> <span property="v:runtime" content="135">135分钟</span><br>\n        <span class="pl">又名:</span> 她们(台)<br>\n        <span class="pl">IMDb链接:</span> <a href="https://www.imdb.com/title/tt3281548" target="_blank" rel="nofollow">tt3281548</a><br>\n\n</div>'
    # xpath = '//*[@id="info"]'
    # nodes = Tree.create_tree(html, xpath)
    # res = AnalysisTree().get_parallel(nodes)
    # print(res)

    html = '<div id="info">\n        <span><span class="pl">导演</span>: <span class="attrs"><a href="/celebrity/1022652/" rel="v:directedBy">格蕾塔·葛韦格</a></span></span><br>\n        <span><span class="pl">编剧</span>: <span class="attrs"><a href="/celebrity/1022652/">格蕾塔·葛韦格</a> / <a href="/celebrity/1037345/">路易莎·梅·奥尔科特</a></span></span><br>\n        <span class="actor"><span class="pl">主演</span>: <span class="attrs"><span><a href="/celebrity/1022004/" rel="v:starring">西尔莎·罗南</a> / </span><span><a href="/celebrity/1053624/" rel="v:starring">艾玛·沃森</a> / </span><span><a href="/celebrity/1378921/" rel="v:starring">弗洛伦丝·皮尤</a> / </span><span><a href="/celebrity/1395069/" rel="v:starring">伊莱扎·斯坎伦</a> / </span><span><a href="/celebrity/1006983/" rel="v:starring">劳拉·邓恩</a> / </span><span style="display: inline;"><a href="/celebrity/1325862/" rel="v:starring">蒂莫西·柴勒梅德</a> / </span><span style="display: inline;"><a href="/celebrity/1054437/" rel="v:starring">梅丽尔·斯特里普</a> / </span><span style="display: inline;"><a href="/celebrity/1027856/" rel="v:starring">鲍勃·奥登科克</a> / </span><span style="display: inline;"><a href="/celebrity/1326707/" rel="v:starring">詹姆斯·诺顿</a> / </span><span style="display: inline;"><a href="/celebrity/1018067/" rel="v:starring">路易·加瑞尔</a> / </span><span style="display: inline;"><a href="/celebrity/1009288/" rel="v:starring">克里斯·库珀</a> / </span><span style="display: inline;"><a href="/celebrity/1009889/" rel="v:starring">崔西·莱茨</a> / </span><span style="display: inline;"><a href="/celebrity/1386474/" rel="v:starring">艾比·奎因</a> / </span><span style="display: inline;"><a href="/celebrity/1366443/" rel="v:starring">萨沙·弗若洛娃</a> / </span><span style="display: inline;"><a href="/celebrity/1351693/" rel="v:starring">莉莉·恩格勒特</a> / </span><span style="display: inline;"><a href="/celebrity/1082829/" rel="v:starring">爱德华德·弗莱彻</a> / </span><span style="display: inline;"><a href="/celebrity/1386049/" rel="v:starring">杰妮·霍蒂谢尔</a> / </span><span style="display: inline;"><a href="/celebrity/1411091/" rel="v:starring">多梅尼克·阿尔迪诺</a> / </span><span style="display: inline;"><a href="/celebrity/1251841/" rel="v:starring">汤姆·斯特拉特福</a> / </span><span style="display: inline;"><a href="/celebrity/1035084/" rel="v:starring">托马斯·马里亚诺</a> / </span><span style="display: inline;"><a href="/celebrity/1421394/" rel="v:starring">哈德莉·罗宾逊</a> / </span><span style="display: inline;"><a href="/celebrity/1421395/" rel="v:starring">杰米·加扎里安</a></span><a href="javascript:;" class="more-actor" title="更多主演" style="display: none;">更多...</a></span></span><br>\n        <span class="pl">类型:</span> <span property="v:genre">剧情</span> / <span property="v:genre">爱情</span><br>\n        <span class="pl">官方网站:</span> <a href="http://www.littlewomen.movie/" rel="nofollow" target="_blank">www.littlewomen.movie/</a><br>\n        <span class="pl">制片国家/地区:</span> 美国<br>\n        <span class="pl">语言:</span> 英语<br>\n        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2020-08-25(中国大陆)">2020-08-25(中国大陆)</span> / <span property="v:initialReleaseDate" content="2019-12-25(美国)">2019-12-25(美国)</span><br>\n        <span class="pl">片长:</span> <span property="v:runtime" content="135">135分钟</span><br>\n        <span class="pl">又名:</span> 她们(台)<br>\n        <span class="pl">IMDb链接:</span> <a href="https://www.imdb.com/title/tt3281548" target="_blank" rel="nofollow">tt3281548</a><br>\n\n</div>'
    # html = '<ul class="celebrities-list from-subject __oneline">\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1022652/" title="格蕾塔·葛韦格 Greta Gerwig" class="">\n      <div class="avatar" style="background-image: url(https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1513870447.95.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1022652/" title="格蕾塔·葛韦格 Greta Gerwig" class="name">格蕾塔·葛韦格</a></span>\n\n      <span class="role" title="导演">导演</span>\n\n    </div>\n  </li>\n\n\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1022004/" title="西尔莎·罗南 Saoirse Ronan" class="">\n      <div class="avatar" style="background-image: url(https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p9684.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1022004/" title="西尔莎·罗南 Saoirse Ronan" class="name">西尔莎·罗南</a></span>\n\n      <span class="role" title="饰 乔 Jo March">饰 乔 Jo March</span>\n\n    </div>\n  </li>\n\n\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1053624/" title="艾玛·沃森 Emma Watson" class="">\n      <div class="avatar" style="background-image: url(https://img3.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1512020567.12.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1053624/" title="艾玛·沃森 Emma Watson" class="name">艾玛·沃森</a></span>\n\n      <span class="role" title="饰 梅格 Meg March">饰 梅格 Meg March</span>\n\n    </div>\n  </li>\n\n\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1378921/" title="弗洛伦丝·皮尤 Florence Pugh" class="">\n      <div class="avatar" style="background-image: url(https://img1.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1517034183.97.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1378921/" title="弗洛伦丝·皮尤 Florence Pugh" class="name">弗洛伦丝·皮尤</a></span>\n\n      <span class="role" title="饰 艾美 Amy March">饰 艾美 Amy March</span>\n\n    </div>\n  </li>\n\n\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1395069/" title="伊莱扎·斯坎伦 Eliza Scanlen" class="">\n      <div class="avatar" style="background-image: url(https://img9.doubanio.com/view/celebrity/s_ratio_celebrity/public/p1530710637.06.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1395069/" title="伊莱扎·斯坎伦 Eliza Scanlen" class="name">伊莱扎·斯坎伦</a></span>\n\n      <span class="role" title="饰 贝斯 Beth March">饰 贝斯 Beth March</span>\n\n    </div>\n  </li>\n\n\n        \n    \n\n    \n  \n  <li class="celebrity">\n    \n\n  <a href="https://movie.douban.com/celebrity/1006983/" title="劳拉·邓恩 Laura Dern" class="">\n      <div class="avatar" style="background-image: url(https://img1.doubanio.com/view/celebrity/s_ratio_celebrity/public/p18559.webp)">\n    </div>\n  </a>\n\n    <div class="info">\n      <span class="name"><a href="https://movie.douban.com/celebrity/1006983/" title="劳拉·邓恩 Laura Dern" class="name">劳拉·邓恩</a></span>\n\n      <span class="role" title="饰 妈妈 Marmee March">饰 妈妈 Marmee March</span>\n\n    </div>\n  </li>\n\n\n  </ul>'
    xpath = '//*[@id="info"]'
    # xpath = '//*[contains(@class, "celebrities-list")]'

    templates = [
        {"key": "value", "tag": "span", "attrib": {"class": "attrs"}, "child": True},
        {"key": "key", "tag": "span", "attrib": {"class": "pl"}}
    ]
    nodes = Tree.create_tree(html, xpath)
    res = AnalysisTree(nodes, templates).get_value()
    print(res)