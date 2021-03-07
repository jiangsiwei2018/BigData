#encoding=utf-8
import numpy as np
import math
import pandas
from pandas import DataFrame


class Tree:
    def __init__(self, parent=None, entropy=None, results=None, nodes={}):
        self.parent = parent
        #所有叶节点的经验熵都是0
        self.entropy = entropy
        self.results = results
        self.nodes = nodes
        

class DecisionTree:
    """"""
    def __init__(self):
        pass

    @staticmethod
    def jy_shang(data, label):
        total = len(data)
        hd = 0
        dtemp = {}
        group = data.groupby([label]).count()
        if isinstance(group, pandas.DataFrame):
            dtemp = dict(group[label])
        elif isinstance(group, pandas.Series):
            dtemp[group.name] = group.values[0]
        for k,v in dtemp.items():
            hd -= (float(v)/total) * math.log(float(v)/total, 2)
        return hd

    @staticmethod
    def tjjy_shang(data, xlabel, ylabel):
        hx = 0
        total = len(data)
        for k, vdata in data.groupby(xlabel):
            vtotal = len(vdata)
            hx += float(vtotal)/total * DecisionTree.jy_shang(vdata, ylabel)
        return hx

    @staticmethod
    def xxzengyi(jingyanshang, tjjingyanshang):
        '''
        hd = DecisionTree.jy_shang(data, ylabel)
        hx = DecisionTree.tjjy_shang(data, xlabel, ylabel)
        '''        
        hd = jingyanshang
        hx = tjjingyanshang
        return hd - hx

    @staticmethod
    def xxzengyibi(xxzengyi, jy_shang_a):
        '''
        ga = DecisionTree.xxzengyi(jingyanshang, tjjingyanshang)
        ha = DecisionTree.jy_shang(data, ylabel, xlabel=alabel)
        '''
        ga = xxzengyi
        ha = jy_shang_a
        return float(ga) / ha
        
    @staticmethod
    def get_label(data, ylabel, C45flag=True):
        '''notes:C45flag=True默认是C45算法，否则为ID3算法'''
        labellist = list(data.columns)
        labellist.remove(ylabel)
        hd = DecisionTree.jy_shang(data, ylabel)
        xxzylist = {}
        for xlabel in labellist:
            hx = DecisionTree.tjjy_shang(data, xlabel, ylabel)
            ga = DecisionTree.xxzengyi(hd, hx)
            if C45flag:
                ha = DecisionTree.jy_shang(data, xlabel)
                xxzylist[xlabel] = DecisionTree.xxzengyibi(ga, ha)
            else:
                xxzylist[xlabel] = ga                                         
        print(xxzylist)
        return max(xxzylist.items(), key=lambda x:x[1])

    @staticmethod
    def get_class(data, ylabel):
        dtemp = {}
        group = data.groupby(ylabel).count()
        if isinstance(group, pandas.DataFrame):
            dtemp = dict(group[ylabel])
        elif isinstance(group, pandas.Series):
            #此种情况是全部为同一分类时
            return group.name
        return max(dtemp.items(), key=lambda x:x[1])[0]

    @staticmethod
    def is_onenode(data, ylabel):
        #进行分类后只有一列，此时类型为Series
        #此种情况是全部为同一分类时
        if isinstance(data.groupby(ylabel).count(), pandas.Series):
            return True
        return False

    @staticmethod
    def build_tree(data, ylabel, min_err=0, min_sample=1):
        '''
        tree.parent为属性A
        tree.nodes为字典，键为属性A的值，值为除A及消耗掉的样本外的属性及样本组成的子树, 
        1)tree.nodes存在时tree.results为None
        2)tree.nodes为空时tree.results存放类别
        '''   
        labellist = list(data.columns)
        labellist.remove(ylabel)
        print(data)
        while labellist:
            #属性是否为空，属性消耗完了，此时只剩下分类标签ylabel时，返回
            if len(labellist) == 0:
                break
            #判断是否是单结点
            if DecisionTree.is_onenode(data, ylabel):
                break 
            #当样本量小于阈值时
            if len(data) <= min_sample:
                break
            node = DecisionTree.get_label(data[labellist + [ylabel]], ylabel)
            label = node[0]
            minival = node[1]
            #当信息增益小于阈值值
            if minival < min_err:
                break
            group = data.groupby(label)
            labellist.remove(label)
            nodes = {}
            for k, vdata in group:
                print('groupby({label}): {k}'.format(label=label, k=k))
                print(vdata)
                #根据属性值划分左右子树
                nodes[k] = DecisionTree.build_tree(vdata[labellist + [ylabel]], ylabel, min_err, min_sample)
            return Tree(entropy=DecisionTree.jy_shang(data, ylabel), parent=label, nodes=nodes)
        return Tree(entropy=DecisionTree.jy_shang(data, ylabel), results=DecisionTree.get_class(data, ylabel))

    @staticmethod
    def predict(sample, tree):
        '''
        input: sample(Series), tree
        output:y class
        '''
        if not tree.nodes:
            return tree.results
        else:
            node = tree.nodes[sample[tree.parent]]
            return DecisionTree.predict(sample, node)


class CartTree(DecisionTree):

    def __init__(self):
        DecisionTree.__init__(self)

    @staticmethod
    def sunshihanshu(data, ylabel, At):
        Ct = 0
        total = len(data)
        for k, vdata in data.groupby(xlabel):
            Nt = len(vdata)
            Ht = CartTree.jy_shang(vdata, ylabel)
            Ct -= Nt * Ht
        return Ct + At      


if __name__ == '__main__':
    d = {'a':[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3],
         'b':[0,0,1,1,0,0,0,1,0,0,0,0,1,1,0],
         'c':[0,0,0,1,0,0,0,1,1,1,1,1,0,0,0],
         'y':[0,0,1,1,0,0,0,1,1,1,1,1,1,1,0]}
    df = DataFrame(d)
    print(df)
    #df.values是一列数组列表
    samples = df.values
    lables = df.columns
    ylabel = 'y'
    tree = DecisionTree.build_tree(df, ylabel, 0.005, 1)
    for sample in samples:
        print(sample, '\tclass:\t', DecisionTree.predict(pandas.Series(sample, index=lables), tree))

 

        
        
    
    