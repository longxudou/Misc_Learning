import math
import numpy as np

capacity = 8
num = 4

res = [0]+[0 for i in range(num)]
w = [0]+[i * i+1 for i in range(num)]  # 1 3 5 10
v = [0]+[2 * i for i in range(num)]  # 0 2 4 6
val = [[0 for i in range(capacity+1)] for  j in range(num+1)]
b = [0]+[0 for i in range(capacity)]


def findMAX():
    for i in range(1,num+1):
        for j in range(1,capacity+1):
            if j < w[i]:
                val[i][j] = val[i - 1][j]
            else:
                val[i][j] = max(val[i - 1][j - w[i]] + v[i], val[i - 1][j])

def findMAX2():
    for i in range(1,num+1):
        for j in range(capacity, w[i]-1,-1):
            try:
                b[j] = max(b[j - w[i]] + v[i], b[j])
                # print j,
            except:
                print j


def TraceBack(i, j):
    print i,j

    if (i >= 0):
        if (val[i][j] == val[i - 1][j]):
            res[i] = 0
            TraceBack(i - 1, j)
        else:
            res[i] = 1
            TraceBack(i - 1, j - w[i])



findMAX()
TraceBack(num, capacity)
print res
print np.array(val)

findMAX2()
print b
