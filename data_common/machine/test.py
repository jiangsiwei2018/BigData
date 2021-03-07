import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets

data = datasets.load_iris()
X = data['data']
y = data['target']
ax = Axes3D(plt.figure())
for c, i, target_name in zip('rgb', [0, 1, 2], data.target_names):
    ax.scatter(X[y == i, 0], X[y == i, 2], c=c, label=target_name)

ax.set_xlabel(data.feature_names[0])
ax.set_xlabel(data.feature_names[1])
ax.set_xlabel(data.feature_names[2])
ax.set_title('Iris')
plt.legend()
plt.show()