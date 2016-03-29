import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.svm import LinearSVC

"""
SUPERVISED LEARNING CLASSIFICATION ALGORITHM
"""


# def representation(X1,X2, y):
#     plt.scatter(X1, X2, c=y)
#     plt.show()
#
#
# def main_clasifier(X, y):
#     """
#     LinearSVC f()
#     :return:
#     """
#     clf = LinearSVC()
#     # print(clf)
#     clf.fit(X, y)
#     print(clf.predict([[5.5,  2.4,  3.8,  1.1]]))

"""
UNSUPERVISED LEARNING
"""
if __name__ == "__main__":
    iris = load_iris()
    X = iris.data
    y = iris.target
    c = iris.target_names
    # print(X[80])
    # print(y[80])
    # print(c)
    # representation(X[:, 0], X[:, 1], y)
    # print(X[0])
    # print(X[:, 1])
    # main_clasifier(X, y)