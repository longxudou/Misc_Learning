import math
import numpy as np

capacity = 8
num = 4

res = [0 for i in range(num)]
w = [i * i for i in range(num)]  # 0 1 4 9
v = [2 * i for i in range(num)]  # 0 1 2 3
val = [[0 for i in range(capacity)] for j in range(num)]


def findMAX():
    for i in range(num):
        for j in range(capacity):
            if j < w[i]:
                val[i][j] = val[i - 1][j]
            else:
                val[i][j] = max(val[i - 1][j - w[i]] + v[i], val[i - 1][j])


def TraceBack(i, j):
    if (i >= 0):
        if (val[i][j] == val[i - 1][j]):
            res[i] = 0
            TraceBack(i - 1, j)
        else:
            res[i] = 1
            TraceBack(i - 1, j - w[i])


findMAX()
TraceBack(num - 1, capacity - 1)
print res
print np.array(val)
