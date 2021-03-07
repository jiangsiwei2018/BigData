# coding=utf-8
from sklearn import preprocessing


class PreProcess:

    """
    预处理：标准化,
    """
    @staticmethod
    def standard_scaler():
        """
        标准化：基于mean和std的标准化
        归一化：将每个特征值归一化到一个固定范围
        :return:
        """
        train_data = [[0, 0], [0, 0], [1, 1], [1, 1]]
        test_data = [[0, 0], [0, 0], [1, 1], [1, 1]]
        # 1. 基于mean和std的标准化
        scaler = preprocessing.StandardScaler().fit(train_data)
        print(scaler)
        s1 = scaler.transform(train_data)
        s2 = scaler.transform(test_data)
        print(s1)
        print(s2)

        # 2. 将每个特征值归一化到一个固定范围
        # feature_range: 定义归一化范围，注用（）括起来
        scaler = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(train_data)
        print(scaler)
        s1 = scaler.transform(train_data)
        s2 = scaler.transform(test_data)
        print(s1)
        print(s2)

        # one-hot编码是一种对离散特征值的编码方式，在LR模型中常用到，用于给线性模型增加非线性能力
        data = [[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]]
        encoder = preprocessing.OneHotEncoder().fit(data)
        print(encoder)
        s2 = encoder.transform(data)
        print(s2)

        # 当你想要计算两个样本的相似度时必不可少的一个操作，就是正则化。
        # 其思想是：首先求出样本的p-范数，然后该样本的所有元素都要除以该范数，这样最终使得每个样本的范数都为1
        X = [[1., -1., 2.], [2., 0., 0.], [0., 1., -1.]]
        X_normalized = preprocessing.normalize(X)
        print(X_normalized)
        # scaler.transform(train_data)
        # scaler.transform(test_data)

    @staticmethod
    def mode_selection():
        """
        参数
        ---
        arrays：样本数组，包含特征向量和标签

        test_size：
        　　float-获得多大比重的测试样本 （默认：0.25）
        　　int - 获得多少个测试样本

        train_size: 同test_size

        random_state:
        　　int - 随机种子（种子固定，实验可复现）
        　　
        shuffle - 是否在分割之前对数据进行洗牌（默认True）

        返回
        ---
        分割后的列表，长度=2*len(arrays),
        　　(train-test split)
        """
        # 作用：将数据集划分为 训练集和测试集
        # 格式：train_test_split(*arrays, **options)
        from sklearn.mode_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


if __name__ == '__main__':
    PreProcess.standard_scaler()
