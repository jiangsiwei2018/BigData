# encoding=utf-8
import hashlib


class HashConsistency(object):
    def __init__(self, name, nodes=None, shards=64, replicas=32):
        # 虚拟节点与真实节点对应关系
        self.name = name,
        self.shards = shards
        self.nodes_map = []
        # 真实节点与虚拟节点的字典映射
        self.nodes_replicas = {}
        # 真实节点
        self.nodes = self.get_nodes(nodes)
        # 每个真实节点创建的虚拟节点的个数
        self.replicas = replicas

        if self.nodes:
            for node in self.nodes:
                self._add_nodes_map(node)
            self._sort_nodes()

    def get_nodes(self, nodes):
        shards = []
        length = len(nodes)
        for i in range(self.shards):
            pos = i % length
            shard = f'{nodes[pos]}_{i}'
            shards.append(shard)
        return shards

    def get_node(self, key):
        """ 根据KEY值的hash值，返回对应的节点
        算法是： 返回最早比key_hash大的节点
        """
        key_hash = self.gen_hash(key)
        # print('%s' % key_hash)
        for node in self.nodes_map:
            if key_hash > node[0]:
                continue
            return node[1]
        return None

    def add_node(self, node):
        # 添加节点
        self._add_nodes_map(node)
        self._sort_nodes()

    def remove_node(self, node):
        # 删除节点
        if node not in self.nodes_replicas.keys():
            pass
        discard_rep_nodes = self.nodes_replicas[node]
        self.nodes_map = filter(lambda x: x[0] not in discard_rep_nodes, self.nodes_map)

    def _add_nodes_map(self, node):
        # 增加虚拟节点到nodes_map列表
        nodes_reps = []
        for i in range(self.replicas):
            rep_node = '%s_%d' % (node, i)
            node_hash = self.gen_hash(rep_node)
            self.nodes_map.append((node_hash, node))
            nodes_reps.append(node_hash)
        # 真实节点与虚拟节点的字典映射
        self.nodes_replicas[node] = nodes_reps

    def _sort_nodes(self):
        # 按顺序排列虚拟节点
        self.nodes_map = sorted(self.nodes_map, key=lambda x: x[0])

    @staticmethod
    def gen_hash(name):
        obj = hashlib.md5("satan@1234sssss".encode("utf-8"))
        obj.update(name.encode('utf-8'))
        return obj.hexdigest()

nodes = [
    '127.0.0.1:7001',
    '127.0.0.1:7002',
    '127.0.0.1:7003',
    '127.0.0.1:7004',
]

h = HashConsistency('aaa', nodes)
for item in h.nodes:
    print(item)
print(h.get_node('mmm'))
