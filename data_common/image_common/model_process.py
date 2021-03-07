# coding=utf-8
import numpy as np
# from sklearn.externals import joblib
import joblib
from sklearn.metrics import confusion_matrix
# from sklearn.datasets import make_blobs
from sklearn.ensemble import RandomForestClassifier
# from sklearn.ensemble import ExtraTreesClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.linear_model import SGDClassifier
# from sklearn.metrics import classification_report
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import cross_val_predict
from sklearn import metrics
from sklearn import svm
from data_common.image_common.config import *
from data_common.image_common.image_process import ImageProcess
from data_common.utils.file_util import file_util
from data_common.utils.pool_util import PoolUtility


class ModelProcess:

    @staticmethod
    def model_save(model, model_path):
        joblib.dump(model, model_path)
        return model

    @staticmethod
    def model_load(model_path):
        return joblib.load(model_path)

    @staticmethod
    def model_predict(model, data):
        return model.predict(data)

    @staticmethod
    def image_PCA_model(x_train, y_train, x_test):
        pca = PCA(n_components=0.9, whiten=True)
        # 理解数据
        pca.fit(x_train, y_train)
        # 降维处理
        x_train_pca = pca.transform(y_train)
        x_test_pca = pca.transform(x_test)
        return x_train_pca, x_test_pca

    @staticmethod
    def model_train(data, labels, model_path):
        """
        """
        print("trainning process >>>>>>>>>>>>>>>>>>>>>>")
        # rbf = svm.SVC(kernel='rbf')
        # rbf.fit(data, labels)
        # linear = svm.SVC(decision_function_shape='ovo', kernel='linear')
        # linear.fit(data, labels)
        rf = RandomForestClassifier(n_estimators=100, max_depth=None,min_samples_split=2, random_state=0)
        rf.fit(data, labels)
        return ModelProcess.model_save(rf, model_path)

    @staticmethod
    def model_test(model, data, label):
        predict_list = ModelProcess.model_predict(model, data)
        print("\ntest process >>>>>>>>>>>>>>>>>>>>>>>>")
        print("test precision: ", metrics.precision_score(label, predict_list, average='weighted')) # precision
        print("test recall: ", metrics.recall_score(label, predict_list, average='weighted')) # recall
        print("test f1 score: ", metrics.f1_score(label, predict_list, average='weighted')) # f1 score
        print("confusion matrix:")
        print(confusion_matrix(label, predict_list)) # 混淆矩阵

    @staticmethod
    def model_data_generate(train_data_path=None, captcha_path=None):
        image_list = []
        label_list = []
        if train_data_path:
            for image, label in ImageProcess.image_train_data_read(train_data_path):
                image_list.append(ImageProcess.feature_transfer(image))
                label_list.append(label)
        if captcha_path:
            for image_name, label, image in ImageProcess.image_captcha_path(captcha_path):
                image_list.append(ImageProcess.feature_transfer(image))
                label_list.append(label)
        return np.array(image_list), np.array(label_list)

    @staticmethod
    def feature_transfer_iter(iter_args):
        image_name, label, image = iter_args
        img = ImageProcess.feature_transfer(image)
        return image_name, label, img

    @staticmethod
    def model_data_generate_iter():
        iter_results = ImageProcess.image_captcha_path(captcha_path, limit=100)
        results = PoolUtility.process_pool_iter(ModelProcess.feature_transfer_iter, iter_results, 5)
        for result in results:
            print(result)


class AutoDefineModel(ModelProcess):

    @staticmethod
    def model_train(data, labels, model_path):
        pass


if __name__ == '__main__':
    ModelProcess.model_data_generate_iter()

    # image_list, label_list = ModelProcess.model_data_generate(train_data_path=train_data_path)
    # ModelProcess.model_train(image_list, label_list, model_path)
    #
    # model = ModelProcess.model_load(model_path)
    #
    # image_list_test, label_list_test = ModelProcess.model_data_generate(captcha_path=test_data_path)
    # ModelProcess.model_test(model, image_list_test, label_list_test)


