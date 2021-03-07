# coding=utf-8

# from gensim.test.utils import common_texts, get_tmpfile
# from gensim.models import Word2Vec
#
# path = get_tmpfile("word2vec.model")
#
# model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
#
# print(model.wv.vectors)
#

import os
from data_common.utils.file_util import FileUtil
from data_common.utils.xpath_util import XPathUtil

path = os.path.dirname(__file__) + '/html.txt'
html = FileUtil.read_file(path)


root = XPathUtil.get_root(html)
tt = []
for item in XPathUtil.get_roots(root, '//*[@class="entrylistItemTitle"]'):
    items = XPathUtil.get_list(item, '//a/@href')
    items2 = XPathUtil.get_list(item, '//a/span')
    # ttt = items[0]
    # ttt2 = items2[0]
    # tt.append((ttt, ttt2))
    for k, v in zip(items, items2):
        v = v.replace('原创', '').strip()
        ss = f'<p><a href="{k}" target="_blank">{v}</a></p>'
        print(ss)
