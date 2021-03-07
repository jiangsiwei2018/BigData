# coding=utf-8

from gensim.test.utils import common_texts
from gensim.models import Word2Vec

print(common_texts)

model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)

# print(model.wv.vectors)
print(model.wv.similar_by_word('human'))


"""
通过model的wv获取 Word2VecKeyedVectors对象
"""