# #coding=utf-8
# import numpy as np
# import pandas as pd
#
# class Mac:
#     def __init__(self):
#         #状态列表
#         self.S = [1,2,3]
#         #状态总数
#         self.T = len(self.S)
#         #观测值列表：红 白 红
#         self.O = [0, 1, 0]
#         #观测值总数
#         self.N = len(self.O)
#         #初始状态概率
#         self.pi = np.array([0.2, 0.4, 0.4])
#         #状态转移概率
#         self.A = np.array([[0.5, 0.2, 0.3],
#                       [0.3, 0.5, 0.2],
#                       [0.2, 0.3, 0.5]])
#         #观测概率分布
#         self.B1 = np.array([[0.5, 0.5],
#                        [0.4, 0.6],
#                        [0.7, 0.3]])
#         self.B = {0:self.B1[:,0],
#                   1:self.B1[:, 1]}
#
#         self.alphalist = []
#         self.beltalist = []
#         self.deltalist = []
#         self.psilist = []
#
#
#     def forword(self):
#         '''
#         pi, A, B, O
#         A = [] nxn状态转移矩阵
#         B 为 观测概率矩阵拆出来的字典
#         O 为观测值
#         1.初始前向概率值
#         '''
#         alpha = np.zeros([self.N, self.T])
#         alpha[:, 0] = np.multiply(self.pi, self.B.get(self.O[0]))
#         for i in range(1, self.T):
#             alpha[:, i] = np.multiply(np.dot(alpha[:, i-1], self.A), self.B.get(self.O[i]))
#             #a = np.dot(self.A.T, alpha[:, i-1])
#             #alpha[:, i] = np.multiply(a, self.B.get(self.O[i]))
#             #a = np.array(np.multiply(pd.DataFrame(self.A), pd.DataFrame(alpha[:, i-1])))
#             #alpha[:, i] = np.multiply(np.sum(a, axis=0), self.B.get(self.O[i]))
#         P = sum(alpha[:, self.T-1])
#         print P, alpha
#         return P,alpha
#
#     def backword(self):
#         #初始化belta
#         belta = np.ones([self.N, self.T])
#         for i in range(self.T-2, -1, -1):
#             #aij*bi*beltai
#             belta[:, i] = np.dot(self.A, np.multiply(self.B.get(self.O[i+1]), belta[:, i+1]))
#         P = sum(np.multiply(self.pi, np.multiply(self.B.get(self.O[0]), belta[:, 0])))
#         print P, belta
#         return P,belta
#
#     def gamma(self, alpha, belta):
#         #alpha = self.forword()[1]
#         #belta = self.backword()[1]
#         gamma = np.zeros([self.N, self.T])
#         for t in range(self.T):
#             temp = np.sum(np.multiply(alpha[t, :], belta[t, :]))
#             for i in range(self.N):
#                 gamma[t, i] = alpha[t, i] * belta[t, i] / float(temp)
#         print gamma
#         return gamma
#
#     def emxi(self, alpha, belta):
#         total = 0
#         emxi = np.zeros([self.T, self.N, self.N])
#         for t in range(self.T-1):
#             for i in range(self.N):
#                 for j in range(self.N):
#                     #total += alpha[t, i] * self.A[i, j] * self.B1[j, self.O[t+1]] * belta[j, t+1]
#                     total += alpha[t, i] * self.A[i,j] * self.B.get(self.O[t+1])[j] * belta[j, t+1]
#             for i in range(self.N):
#                 for j in range(self.N):
#                     emxi[t, i, j] = alpha[t, i] * self.A[i,j] * self.B.get(self.O[t+1])[j] * belta[j, t+1] / float(total)
#         print emxi
#         return emxi
#
#
#     #def verbit(self):
#         #delta = np.multiply(self.pi, self.B.get(self.O[0]))
#         #psi = np.zeros(self.T)
#         #self.deltalist.append(delta)
#         #self.psilist.append(psi)
#         #print delta
#         #for i in range(1,self.T):
#             #t = np.multiply(self.A.T, delta).T
#             #delta = np.multiply(np.max(t, axis=0), self.B.get(self.O[i]))
#             #psi = np.argmax(t, axis=0)
#             #self.deltalist.append(delta)
#             #self.psilist.append(psi)
#             #print delta
#             #print psi
#         #I = [0] * self.N
#         #P = max(delta)
#         #I[self.N-1] = np.argmax(psi)
#         #print P, I
#         #print self.deltalist
#         #print self.psilist
#         #for t in range(self.T-2, -1, -1):
#             #I[t] = self.psilist[t+1][I[t+1]]
#             #print I
#         #return I
#
#     def verbit(self):
#         delta = np.zeros([self.N, self.T])
#         psi = np.zeros([self.N, self.T])
#         delta[:, 0] = np.multiply(self.pi, self.B.get(self.O[0]))
#         psi[:, 0] = np.zeros(self.N)
#         for i in range(1,self.T):
#             temp = np.array(np.multiply(pd.DataFrame(self.A), pd.DataFrame(delta[:, i-1])))
#             delta[:, i] = np.multiply(np.max(temp, axis=0), self.B.get(self.O[i]))
#             psi[:, i] = np.argmax(temp, axis=0)
#         I = np.zeros(self.T)
#         P = max(delta[:, self.T-1])
#         I[self.T-1] = np.argmax(psi[:, self.T-1 ])
#         for t in range(self.T-2, -1, -1):
#             I[t] = psi[:, t+1][I[t+1]]
#         print P, I
#         return P,I
#
#
#
# class HMM:
#     def __init__(self, Ann, Bnm, Pi, O):
#         self.A = np.array(Ann, np.float)
#         self.B = np.array(Bnm, np.float)
#         self.Pi = np.array(Pi, np.float)
#         self.O = np.array(O, np.float)
#         self.N = self.A.shape[0]
#         self.M = self.B.shape[1]
#
#     def viterbi(self):
#         # given O,lambda .finding I
#
#         T = len(self.O)
#         I = np.zeros(T, np.float)
#
#         delta = np.zeros((T, self.N), np.float)
#         psi = np.zeros((T, self.N), np.float)
#
#         for i in range(self.N):
#             delta[0, i] = self.Pi[i] * self.B[i, self.O[0]]
#             psi[0, i] = 0
#
#         for t in range(1, T):
#             for i in range(self.N):
#                 delta[t, i] = self.B[i,self.O[t]] * np.array( [delta[t-1,j] * self.A[j,i]
#                                                                for j in range(self.N)] ).max()
#                 psi[t,i] = np.array( [delta[t-1,j] * self.A[j,i]
#                                       for j in range(self.N)] ).argmax()
#
#         P_T = delta[T-1, :].max()
#         I[T-1] = delta[T-1, :].argmax()
#
#         for t in range(T-2, -1, -1):
#             I[t] = psi[t+1, I[t+1]]
#
#         return I
#     def forward(self):
#         T = len(self.O)
#         alpha = np.zeros((T, self.N), np.float)
#
#         for i in range(self.N):
#             alpha[0,i] = self.Pi[i] * self.B[i, self.O[0]]
#
#         for t in range(T-1):
#             for i in range(self.N):
#                 summation = 0   # for every i 'summation' should reset to '0'
#                 for j in range(self.N):
#                     summation += alpha[t,j] * self.A[j,i]
#                 alpha[t+1, i] = summation * self.B[i, self.O[t+1]]
#
#         summation = 0.0
#         for i in range(self.N):
#             summation += alpha[T-1, i]
#         Polambda = summation
#         return Polambda,alpha
#     def backward(self):
#         T = len(self.O)
#         beta = np.zeros((T, self.N), np.float)
#         for i in range(self.N):
#             beta[T-1, i] = 1.0
#
#         for t in range(T-2,-1,-1):
#             for i in range(self.N):
#                 summation = 0.0     # for every i 'summation' should reset to '0'
#                 for j in range(self.N):
#                     summation += self.A[i,j] * self.B[j, self.O[t+1]] * beta[t+1,j]
#                 beta[t,i] = summation
#
#         Polambda = 0.0
#         for i in range(self.N):
#             Polambda += self.Pi[i] * self.B[i, self.O[0]] * beta[0, i]
#         return Polambda, beta
#
#     def compute_gamma(self,alpha,beta):
#         T = len(self.O)
#         gamma = np.zeros((T, self.N), np.float)       # the probability of Ot=q
#         for t in range(T):
#             for i in range(self.N):
#                 gamma[t, i] = alpha[t,i] * beta[t,i] / sum(
#                     alpha[t,j] * beta[t,j] for j in range(self.N) )
#         return gamma
#
#     def compute_xi(self,alpha,beta):
#         T = len(self.O)
#         xi = np.zeros((T-1, self.N, self.N), np.float)  # note that: not T
#         for t in range(T-1):   # note: not T
#             for i in range(self.N):
#                 for j in range(self.N):
#                     numerator = alpha[t,i] * self.A[i,j] * self.B[j,self.O[t+1]] * beta[t+1,j]
#                     # the multiply term below should not be replaced by 'nummerator'，
#                     # since the 'i,j' in 'numerator' are fixed.
#                     # In addition, should not use 'i,j' below, to avoid error and confusion.
#                     denominator = sum( sum(
#                         alpha[t,i1] * self.A[i1,j1] * self.B[j1,self.O[t+1]] * beta[t+1,j1]
#                         for j1 in range(self.N) )   # the second sum
#                                        for i1 in range(self.N) )    # the first sum
#                     xi[t,i,j] = numerator / denominator
#         return xi
#
#     def Baum_Welch(self):
#         # given O list finding lambda model(can derive T form O list)
#         # also given N, M,
#         T = len(self.O)
#         V = [k for k in range(self.M)]
#
#         # initialization - lambda
#         self.A = np.array(([[0,1,0,0],[0.4,0,0.6,0],[0,0.4,0,0.6],[0,0,0.5,0.5]]), np.float)
#         self.B = np.array(([[0.5,0.5],[0.3,0.7],[0.6,0.4],[0.8,0.2]]), np.float)
#
#         # mean value may not be a good choice
#         self.Pi = np.array(([1.0 / self.N] * self.N), np.float)  # must be 1.0 , if 1/3 will be 0
#         # self.A = np.array([[1.0 / self.N] * self.N] * self.N) # must array back, then can use[i,j]
#         # self.B = np.array([[1.0 / self.M] * self.M] * self.N)
#
#         x = 1
#         delta_lambda = x + 1
#         times = 0
#         # iteration - lambda
#         while delta_lambda > x:  # x
#             Polambda1, alpha = self.forward()           # get alpha
#             Polambda2, beta = self.backward()            # get beta
#             gamma = self.compute_gamma(alpha,beta)     # use alpha, beta
#             xi = self.compute_xi(alpha,beta)
#
#             lambda_n = [self.A,self.B,self.Pi]
#
#
#             for i in range(self.N):
#                 for j in range(self.N):
#                     numerator = sum(xi[t,i,j] for t in range(T-1))
#                     denominator = sum(gamma[t,i] for t in range(T-1))
#                     self.A[i, j] = numerator / denominator
#
#             for j in range(self.N):
#                 for k in range(self.M):
#                     numerator = sum(gamma[t,j] for t in range(T) if self.O[t] == V[k] )  # TBD
#                     denominator = sum(gamma[t,j] for t in range(T))
#                     self.B[i, k] = numerator / denominator
#
#             for i in range(self.N):
#                 self.Pi[i] = gamma[0,i]
#
#             # if sum directly, there will be positive and negative offset
#             delta_A = map(abs, lambda_n[0] - self.A)  # delta_A is still a matrix
#             delta_B = map(abs, lambda_n[1] - self.B)
#             delta_Pi = map(abs, lambda_n[2] - self.Pi)
#             delta_lambda = sum([ sum(sum(delta_A)), sum(sum(delta_B)), sum(delta_Pi) ])
#             times += 1
#             print times
#
#         return self.A, self.B, self.Pi
#
#
#     def forward_with_scale(self):
#         T = len(self.O)
#         alpha_raw = np.zeros((T, self.N), np.float)
#         alpha = np.zeros((T, self.N), np.float)
#         c = [i for i in range(T)]  # scaling factor; 0 or sequence doesn't matter
#
#         for i in range(self.N):
#             alpha_raw[0,i] = self.Pi[i] * self.B[i, self.O[0]]
#
#         c[0] = 1.0 / sum(alpha_raw[0,i] for i in range(self.N))
#         for i in range(self.N):
#             alpha[0, i] = c[0] * alpha_raw[0,i]
#
#         for t in range(T-1):
#             for i in range(self.N):
#                 summation = 0.0
#                 for j in range(self.N):
#                     summation += alpha[t,j] * self.A[j, i]
#                 alpha_raw[t+1, i] = summation * self.B[i, self.O[t+1]]
#
#             c[t+1] = 1.0 / sum(alpha_raw[t+1,i1] for i1 in range(self.N))
#
#             for i in range(self.N):
#                 alpha[t+1, i] = c[t+1] * alpha_raw[t+1, i]
#         return alpha, c
#
#
#     def backward_with_scale(self,c):
#         T = len(self.O)
#         beta_raw = np.zeros((T, self.N), np.float)
#         beta = np.zeros((T, self.N), np.float)
#         for i in range(self.N):
#             beta_raw[T-1, i] = 1.0
#             beta[T-1, i] = c[T-1] * beta_raw[T-1, i]
#
#         for t in range(T-2,-1,-1):
#             for i in range(self.N):
#                 summation = 0.0
#                 for j in range(self.N):
#                     summation += self.A[i,j] * self.B[j, self.O[t+1]] * beta[t+1,j]
#                 beta[t,i] = c[t] * summation   # summation = beta_raw[t,i]
#         return beta
#     def Baum_Welch_with_scale(self):
#         T = len(self.O)
#         V = [k for k in range(self.M)]
#
#         # initialization - lambda   ,  should be float(need .0)
#         self.A = np.array([[0.2,0.2,0.3,0.3],[0.2,0.1,0.6,0.1],[0.3,0.4,0.1,0.2],[0.3,0.2,0.2,0.3]])
#         self.B = np.array([[0.5,0.5],[0.3,0.7],[0.6,0.4],[0.8,0.2]])
#
#         x = 5
#         delta_lambda = x + 1
#         times = 0
#         # iteration - lambda
#         while delta_lambda > x:  # x
#             alpha,c = self.forward_with_scale()
#             beta = self.backward_with_scale(c)
#
#             lambda_n = [self.A,self.B,self.Pi]
#
#             for i in range(self.N):
#                 for j in range(self.N):
#                     numerator_A = sum(alpha[t,i] * self.A[i,j] * self.B[j, self.O[t+1]]
#                                       * beta[t+1,j] for t in range(T-1))
#                     denominator_A = sum(alpha[t,i] * beta[t,i] / c[t] for t in range(T-1))
#                     self.A[i, j] = numerator_A / denominator_A
#
#             for j in range(self.N):
#                 for k in range(self.M):
#                     numerator_B = sum(alpha[t,j] * beta[t,j] / c[t]
#                                       for t in range(T) if self.O[t] == V[k] )  # TBD
#                     denominator_B = sum(alpha[t,j] * beta[t,j] / c[t] for t in range(T))
#                     self.B[j, k] = numerator_B / denominator_B
#
#             # Pi have no business with c
#             denominator_Pi = sum(alpha[0,j] * beta[0,j] for j in range(self.N))
#             for i in range(self.N):
#                 self.Pi[i] = alpha[0,i] * beta[0,i] / denominator_Pi
#                 #self.Pi[i] = gamma[0,i]
#
#             # if sum directly, there will be positive and negative offset
#             delta_A = map(abs, lambda_n[0] - self.A)  # delta_A is still a matrix
#             delta_B = map(abs, lambda_n[1] - self.B)
#             delta_Pi = map(abs, lambda_n[2] - self.Pi)
#             delta_lambda = sum([ sum(sum(delta_A)), sum(sum(delta_B)), sum(delta_Pi) ])
#
#             times += 1
#             print times
#
#         return self.A, self.B, self.Pi
#
#
#     # for multiple sequences of observations symbols(with scaling alpha & beta)
#     # out of class HMM, independent function
#     def modified_Baum_Welch_with_scale(O_set):
#         # initialization - lambda
#         A = np.array([[0.2,0.2,0.3,0.3],[0.2,0.1,0.6,0.1],[0.3,0.4,0.1,0.2],[0.3,0.2,0.2,0.3]])
#         B = np.array([[0.2,0.2,0.3,0.3],[0.2,0.1,0.6,0.1],[0.3,0.4,0.1,0.2],[0.3,0.2,0.2,0.3]])
#         # B = np.array([[0.5,0.5],[0.3,0.7],[0.6,0.4],[0.8,0.2]])
#         Pi = [0.25,0.25,0.25,0.25]
#
#         # computing alpha_set, beta_set, c_set
#         O_length = len(O_set)
#         whatever = [j for j in range(O_length)]
#         alpha_set, beta_set = whatever, whatever
#         c_set = [j for j in range(O_length)]  # can't use whatever, the c_set will be 3d-array ???
#
#         N = A.shape[0]
#         M = B.shape[1]
#         T = [j for j in range(O_length)]   # can't use whatever, the beta_set will be 1d-array ???
#         for i in range(O_length):
#             T[i] = len(O_set[i])
#         V = [k for k in range(M)]
#
#         x = 1
#         delta_lambda = x + 1
#         times = 0
#         while delta_lambda > x:   # iteration - lambda
#             lambda_n = [A, B]
#             for i in range(O_length):
#                 alpha_set[i], c_set[i] = HMM(A, B, Pi, O_set[i]).forward_with_scale()
#                 beta_set[i] = HMM(A, B, Pi, O_set[i]).backward_with_scale(c_set[i])
#
#             for i in range(N):
#                 for j in range(N):
#
#                     numerator_A = 0.0
#                     denominator_A = 0.0
#                     for l in range(O_length):
#
#                         raw_numerator_A = sum( alpha_set[l][t,i] * A[i,j] * B[j, O_set[l][t+1]]
#                                     * beta_set[l][t+1,j] for t in range(T[l]-1) )
#                         numerator_A += raw_numerator_A
#
#                         raw_denominator_A = sum( alpha_set[l][t,i] * beta_set[l][t,i] / c_set[l][t]
#                                      for t in range(T[l]-1) )
#                         denominator_A += raw_denominator_A
#
#                     A[i, j] = numerator_A / denominator_A
#
#             for j in range(N):
#                 for k in range(M):
#
#                     numerator_B = 0.0
#                     denominator_B = 0.0
#                     for l in range(O_length):
#                         raw_numerator_B = sum( alpha_set[l][t,j] * beta_set[l][t,j]
#                                     / c_set[l][t] for t in range(T[l]) if O_set[l][t] == V[k] )
#                         numerator_B += raw_numerator_B
#
#                         raw_denominator_B = sum( alpha_set[l][t,j] * beta_set[l][t,j]
#                                     / c_set[l][t] for t in range(T[l]) )
#                         denominator_B += raw_denominator_B
#                     B[j, k] = numerator_B / denominator_B
#
#             # Pi should not need to computing in this case,
#             # in other cases, will get some corresponding Pi
#
#             # if sum directly, there will be positive and negative offset
#             delta_A = map(abs, lambda_n[0] - A)  # delta_A is still a matrix
#             delta_B = map(abs, lambda_n[1] - A)
#             delta_lambda = sum([ sum(sum(delta_A)), sum(sum(delta_B)) ])
#
#             times += 1
#             print times
#
#         return A, B
# if __name__ == '__main__':
#     alpha = Mac().forword()[-1]
#     belta = Mac().backword()[-1]
#     #Mac().verbit()
#     Mac().gamma(alpha, belta)
#     Mac().emxi(alpha, belta)
#     #Mac().backward()
#