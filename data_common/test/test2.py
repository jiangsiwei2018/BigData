import copy
D = {'a': 1, 'b': [3, 5]}
D1 = copy.copy(D)
D2 = copy.deepcopy(D)

D['b'][0] = 4
print(D)
print(D1)
print(D2)


# from skimage import io, data

# img = data.chelsea()
# io.imshow(img)

# io.show()
#
# print(type(img))    # 类型
# print(img.shape)    # 形状
# print(img.shape[0]) # 图片宽度
# print(img.shape[1]) # 图片高度
# print(img.shape[2]) # 图片通道数
# print(img.size)     # 显示总像素个数
# print(img.max())    # 最大像素值
# print(img.min())    # 最小像素值
# print(img.mean())   # 像素平均值

#
# import numpy as np
#
# arr1 = np.array([1, 0])
# arr2 = np.array([1, 1])
#
# arr3 = arr1 + arr2

# x = np.linspace(0, 3, 3, endpoint=False)  # 加密
# y = np.linspace(0, 3, 3, endpoint=False)
# X, Y = np.meshgrid(x, y)
# Y = Y.flatten()
# X = X.flatten()
# tense_points = np.vstack((X, Y)).transpose()
# print(tense_points)

# Y,X =np.mgrid[7:9,0:3]
# # print(B.shape)#(2,2,3)
# print(np.reshape(X,  6))
# print(np.reshape(Y,  6))
# for dos in zip(X.reshape(6), Y.reshape(6)):
#     print(dos)




