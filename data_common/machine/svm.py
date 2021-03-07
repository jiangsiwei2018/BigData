# #coding=utf-8
# import numpy as np
#
# ########################################################################
# class SVM:
#
#     #----------------------------------------------------------------------
#     def __init__(self, dataset, labels, C, toler, kernel_option):
#         #训练集
#         self.train_x = np.mat(dataset)
#         #训练标签
#         self.train_y = np.mat(labels).T
#         #惩罚系数
#         self.C = C
#         #容忍度
#         self.toler = toler
#         #样本数
#         self.n_samples = np.shape(dataset)[0]
#         self.alphas = np.mat(np.zeros(shape=(self.n_samples, 1)))
#         self.b = 0
#         #保存E的缓存
#         self.error_tmp = np.mat(np.zeros(shape=(self.n_samples, 2)))
#         #选用的核函数及其参数
#         self.kernel_opt = kernel_option
#         #核函数的输出
#         self.kernel_mat = cal_kernel(self.train_x, self.kernel_opt)
#
# #----------------------------------------------------------------------
# #样本的核函数矩阵
# def cal_kernel(train_x, kernel_option):
#     num = np.shape(train_x)[0]
#     kernel_martrix = np.mat(np.zeros(shape=(num, num)))
#     for i in xrange(num):
#         kernel_martrix[i, :] = cal_kernel_samples(train_x, train_x[i, :], kernel_option)
#     return kernel_martrix
#
#
# #----------------------------------------------------------------------
# def cal_kernel_samples(train_x, train_x_i, kernel_option):
#     #核函数的类型， 分为rbf和其他
#     kernel_type = kernel_option[0]
#     #样本数
#     num = np.shape(train_x)[0]
#
#     #rbf为高斯核函数
#     if kernel_type == 'rbf':
#         sigma = kernel_option[1]
#         if sigma == 0:
#             sigma = 1.0
#         kernel_samples = np.array(np.zeros(num))
#         for i in xrange(num):
#             diff = train_x[i, :] - train_x_i
#             kernel_samples[i] = np.exp(diff * diff.T / (-2.0 * sigma **2))
#         #diff = train_x - train_x_i
#         #kernel_samples = np.exp(np.diag(diff * diff.T)/(-2.0 * sigma ** 2))
#     else:
#         kernel_samples = train_x * train_x_i.T
#     return kernel_samples
#
# #----------------------------------------------------------------------
# def  SVM_training(train_x, train_y, C, toler, max_iter, kernel_option=('rbf', 0.431029)):
#     #初始化分类器
#     svm = SVM(train_x, train_y, C, toler, kernel_option)
#     #开始训练
#     entireset = True
#     alpha_paris_changed = 0
#     iteration = 0
#     while (iteration < max_iter) and (alpha_paris_changed > 0 or entireset):
#         print 'iteration:\t',iteration
#         alpha_paris_changed = 0
#         if entireset:
#             for x in xrange(svm.n_samples):
#                 alpha_paris_changed += choose_and_update(svm, x)
#                 iteration  += 1
#         else:
#             bound_samples = []
#             for i in range(svm.n_samples):
#                 if svm.alphas[i, 0] > 0 and svm.alphas[i,0] < svm.C:
#                     bound_samples.append(i)
#             for x in bound_samples:
#                 alpha_paris_changed += choose_and_update(svm, x)
#             iteration += 1
#         #在所有样本和非边界样本之间交替
#         if entireset:
#             entireset = False
#         elif alpha_paris_changed == 0:
#             entireset = True
#     return svm
#
# #----------------------------------------------------------------------
# def cal_error(svm, alpha_k):
#     print np.multiply(svm.alphas, svm.train_y).T
#     print svm.kernel_mat[:, alpha_k]
#
#     output_k = float(np.multiply(svm.alphas, svm.train_y).T * svm.kernel_mat[:, alpha_k] + svm.b)
#     return output_k - float(svm.train_y[alpha_k])
#
# #----------------------------------------------------------------------
# def update_error_tmp(svm, alpha_k):
#     error = cal_error(svm, alpha_k)
#     svm.error_tmp[alpha_k] = [1, error]
#
# def select_second_sample_j(svm, alpha_i, error_i):
#     svm.error_tmp[alpha_i] = [1, error_i]
#     candidate_alphalist = np.nonzero(svm.error_tmp[:, 0].A)[0]
#
#     maxstep = 0
#     alpha_j = 0
#     error_j = 0
#     if len(candidate_alphalist) > 1:
#         for alpha_k in candidate_alphalist:
#             if alpha_k == alpha_i:
#                 continue
#             error_k = cal_error(svm, alpha_k)
#             if abs(error_k - error_i) > maxstep:
#                 maxstep = abs(error_k -error_i)
#                 alpha_j = alpha_k
#                 error_j == error_k
#     else:
#         alpha_j = alpha_i
#         while alpha_j == alpha_i:
#             alpha_j = int(np.random.uniform(0, svm.n_samples))
#         error_j = cal_error(svm, alpha_j)
#     return alpha_j, error_j
#
#
# #----------------------------------------------------------------------
# def choose_and_update(svm, alpha_i):
#     error_i = cal_error(svm, alpha_i)
#     #1不满足KKT条件时，更新第二个alpha变量
#     if ((svm.train_y[alpha_i] * error_i < -svm.toler) and (svm.alphas[alpha_i] < svm.C)) \
#        or ((svm.train_y[alpha_i] * error_i > svm.toler) and (svm.alphas[alpha_i] > 0)):
#         alpha_j, error_j = select_second_sample_j(svm, alpha_i, error_i)
#         alpha_i_old = svm.alphas[alpha_i].copy()
#         alpha_j_old = svm.alphas[alpha_j].copy()
#         #2计算上下界
#         if svm.train_y[alpha_i] != svm.train_y[alpha_j]:
#             L = max(0, svm.alphas[alpha_j] - svm.alphas[alpha_i])
#             H = min(svm.C, svm.C + svm.alphas[alpha_j] - svm.alphas[alpha_i])
#         else:
#             L = min(0, svm.alphas[alpha_j] + svm.alphas[alpha_i]- svm.C)
#             H = max(svm.C, svm.alphas[alpha_j] + svm.alphas[alpha_i])
#         if L == H:
#             return 0
#         #3计算eta
#         print svm.kernel_mat
#         eta = 2.0 * svm.kernel_mat[alpha_i, alpha_j] - svm.kernel_mat[alpha_i, alpha_i] - svm.kernel_mat[alpha_j, alpha_j]
#         if eta >= 0:
#             return 0
#         #4跟新alpha_j
#         svm.alphas[alpha_j] -= svm.train_y[alpha_j] * (error_i - error_j) / eta
#         #5确定最终的alpha_j
#         if svm.alphas[alpha_j] > H:
#             svm.alphas[alpha_j] = H
#         if svm.alphas[alpha_j] < L:
#             svm.alphas[alpha_j] = L
#         #6判断是否结束
#         if  abs(alpha_j_old - svm.alphas[alpha_j]) < 0.00001:
#             update_error_tmp(svm, alpha_j)
#             return 0
#
#         #7更新alpha_i
#         svm.alphas[alpha_i] += svm.train_y[alpha_i] * svm.train_y[alpha_j] * (alpha_j_old - svm.alphas[alpha_j])
#         #8更新b
#         b1 = svm.b - error_i - svm.train_y[alpha_i] * (svm.alphas[alpha_i] - alpha_i_old) * svm.kernel_mat[alpha_i, alpha_i] \
#              - svm.train_y[alpha_j] * (svm.alphas[alpha_j] - alpha_j_old) * svm.kernel_mat[alpha_i, alpha_j]
#         b2 = svm.b - error_j - svm.train_y[alpha_i] * (svm.alphas[alpha_i] - alpha_i_old) * svm.kernel_mat[alpha_i, alpha_j] \
#              - svm.train_y[alpha_j] * (svm.alphas[alpha_j] - alpha_j_old) * svm.kernel_mat[alpha_j, alpha_j]
#         if svm.alphas[alpha_i] > 0 and svm.alphas[alpha_i] < svm.C:
#             svm.b = b1
#         if svm.alphas[alpha_j] > 0 and svm.alphas[alpha_j] < svm.C:
#             svm.b = b2
#         else:
#             svm.b = (b1 + b2) / 2.0
#         #跟新error
#         update_error_tmp(svm, alpha_j)
#         update_error_tmp(svm, alpha_i)
#         return 1
#     else:
#         return 0
#
# #----------------------------------------------------------------------
# def svm_predict(svm, test_sample_x):
#     kernel_samples = cal_kernel_samples(svm.train_x, test_sample_x, svm.kernel_opt)
#     predict = kernel_samples * np.multiply(svm.train_y, svm.alphas) + svm.b
#     return predict
#
# #----------------------------------------------------------------------
# def cal_accuracy(svm, test_x, test_y):
#     n_samples = np.shape(test_x)[0]
#     correct = 0.0
#     for i in xrange(n_samples):
#         predict = svm_predict(svm, test_x[i, :])
#         if np.sign(predict) == np.sign(test_y[i]):
#             correct += 1
#     return correct / n_samples
#
# if __name__ == '__main__':
#     dateset  = np.array([[3,3], [4,3], [1,1]])
#     labels = [1, 1, -1]
#     C = 0.6
#     toler = 0.001
#     max_iter = 500
#     svm_model = SVM_training(dateset, labels, C, toler, max_iter, kernel_option=('rbf', 0.431029))
#     accuracy = cal_accuracy(svm_model, dateset, labels)
#     print(accuracy)