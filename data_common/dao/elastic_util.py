# coding=utf-8

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from data_common.designs.singleton import SingletonType
from data_common.utils.log_util import Logger

# 别名操作
# 索引操作
# 基本操作：增删查改

class ElasticSearchUtil(metaclass=SingletonType):

    def __init__(self, host, username=None, password=None):
        self.host = host
        self.username = username
        self.password = password
        self.client = None

    def connection(self):
        self.client = Elasticsearch(self.host, http_auth=(self.username, self.password))

    def index_exists(self, index):
        return self.client.indices.get(index)

    def index_create(self, index, mapping, **params):
        self.client.indices.create(index, body=mapping, params=params)

    def index_delete(self, index):
        self.client.indices.delete(index)

    def get_indices_by_alias(self, alias):
        """
        [{'alias': 'wocao', 'index': 'person', 'filter': '-', 'routing.index': '-', 'routing.search': '-'},
         {'alias': 'wocao', 'index': 'person1', 'filter': '-', 'routing.index': '-', 'routing.search': '-'}]
        """
        index_list = self.client.cat.aliases(name=alias, format='json')
        index_list = [index['index'] for index in index_list]
        return index_list

    def refresh(self, index, **kwargs):
        self.client.refresh(index, **kwargs)

    def alias_actions(self, actions):
        """
        {
          "actions" : [{"remove" : {"index" : "student" , "alias" : "in1"}}],
          "actions" : [{"add" : {"index" : "student" , "alias" : "in2"}}]
        }
        :param actions:
        :return:
        """
        self.client.indices.update_aliases(actions)

    def alias_create(self, index, alias):
        index = index if isinstance(index, list) else [index]
        self.client.indices.put_alias(index=index, name=alias)

    def alias_delete(self, index, alias):
        index = index if isinstance(index, list) else [index]
        self.client.indices.delete_alias(index=index, name=alias)

    def alias_index_list(self, index):
        index = index if isinstance(index, list) else [index]
        return self.client.indices.get_alias(index=index)

    def command(self, opt, *args, **kwargs):
        opt = getattr(self.client, opt, None)
        if opt:
            Logger.debug(f'{opt}\t{args}\t{kwargs}')
            return opt(*args, **kwargs)

    @staticmethod
    def format_result(results):
        for hit in results['hits']['hits']:
            return hit['_source']

    def doc_search(self, index, body):
        """
        TODO 循环游标的处理
        :param index:
        :param body:
        :return:
        """
        results = self.command('search', index=index, body=body)
        return self.format_result(results)

    def doc_search_multi(self, index_and_query):
        # self.client.msearch()
        pass

    def doc_search_all(self, index):
        return self.doc_search(index, body={"query": {"match_all": {}}})

    def doc_get_by_id(self, index, _id):
        results = self.command('get', index=index, id=_id)
        return self.format_result(results)

    def insert(self, index, body):
        pass

    def insert_multi(self, index, value_list=None, _id='id'):
        actions = []
        for value in value_list:
            action = {
                "_index": index,
                "_type": '_doc',
                "_id": value[_id] if _id in value else '',
                "_source": value
            }
            actions.append(action)
            # 批量处理
        success = helpers.bulk(self.client, actions, index=index)
        return success

    def update(self):
        pass

    def update_by_script(self):
        pass

    def update_nested(self):
        pass


class EsDoc:
    """
    一.关于别名的操作
    es.indices.put_alias，为一个或多个索引创建别名，查询多个索引的时候，可以使用这个别名
    print(es.indices.put_alias(index='p3', name='p3_alias'))  # 为单个索引创建别名
    print(es.indices.put_alias(index=['p3', 'p2'], name='p23_alias'))  # 为多个索引创建同一个别名，联查用
    es.indices.delete_alias，删除一个或多个别名
    #必须指定索引和要删除的别名，因为一个索引可能对应多个别名 index和name的参数必须同时传入
    pprint(es.indices.delete_alias(index=['person'],name='wocao')) #{'acknowledged': True}
    pprint(es.indices.delete_alias(index=['person','person1'],name='wocao')) #{'acknowledged': True}
    es.indices.get_alias，查询索引所存在的别名
    print(es.indices.get_alias(index=['person1']))  #{'person1': {'aliases': {'wocao': {}}}}

    print(es.indices.get_alias(index=['p2', 'p3']))

    es.indices.exists_alias,判断一个索引是否存在某个别名
    print(es.indices.exists_alias(name='wocao',index='person'))  #True

    二. 查看索引的相关配置
    　　es.indices.get_mapping，检索索引或索引/类型的映射定义

    pprint(es.indices.get_mapping(index='person'))
    　　es.indices.get_settings，检索一个或多个（或所有）索引的设置。

    pprint(es.indices.get_settings(index='person'))
    　　es.indices.get，允许检索有关一个或多个索引的信息。

     print(es.indices.get(index='person'))    # 查询指定索引是否存在
     print(es.indices.get(index=['person', 'person1']))

     es.indices.get_field_mapping，检索特定字段的映射信息。

    其他操作：　　　
    es.indices.exists_type，检查索引/索引中是否存在类型/类型。
    es.indices.flush，明确的刷新一个或多个索引。
    es.indices.get_template，按名称检索索引模板。
    es.indices.open，打开一个封闭的索引以使其可用于搜索。
    es.indices.close，关闭索引以从群集中删除它的开销。封闭索引被阻止进行读/写操作。
    es.indices.clear_cache，清除与一个或多个索引关联的所有缓存或特定缓存。
    es.indices.get_uprade，监控一个或多个索引的升级程度。
    es.indices.put_mapping，注册特定类型的特定映射定义。
    es.indices.put_settings，实时更改特定索引级别设置。
    es.indices.put_template，创建一个索引模板，该模板将自动应用于创建的新索引。
    es.indices.rollove，当现有索引被认为太大或太旧时，翻转索引API将别名转移到新索引。API接受单个别名和条件列表。别名必须仅指向单个索引。如果索引满足指定条件，则创建新索引并切换别名以指向新别名。
    es.indices.segments，提供构建Lucene索引（分片级别）的低级别段信息
    """