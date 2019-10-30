import random
import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMaximize, LpMinimize, lpSum, LpVariable, LpProblem, LpStatus, LpContinuous, value
import time
import copy

random.seed(0)

def data_generator(num,threshold):
    X = set([i for i in range(num)]) # 0,1,2,....,num-2,num-1
    F = []
    selected_index = set()
    s0_index = set(random.sample([i for i in range(num)],threshold))
    F.append(s0_index)
    selected_index=selected_index|s0_index
    #Feasible subset, size:y
    while True:
        if num - len(selected_index) < threshold:
            new_index = X - set(selected_index)
            F.append(new_index)
            break
        sample_size = random.randint(1, threshold)
        sample_size_former = random.randint(1, sample_size)
        sample_num_from_former=set(random.sample(list(selected_index),sample_size_former))
        sample_num_from_later=set(random.sample(list(X-selected_index),sample_size-sample_size_former))
        Si_index=sample_num_from_former|sample_num_from_later
        if Si_index in F:
            continue
        F.append(Si_index)
        selected_index=selected_index|Si_index
    #remain subset, |F|-y
    while len(F) != num:
        size = random.randint(1, max(int(threshold/2), 5))
        new_index=set(random.sample([i for i in range(num)], size))
        if new_index in F:
            continue
        F.append(set(new_index))
    return X, F


def greedy_set_cover(X, _F):
    start = time.clock()

    F=copy.deepcopy(_F)
    result = []
    covered = set()

    while covered != X:
        max = 0
        candidate = None
        for f in F:
            length = len(f - covered)
            if length > max:
                candidate = f
                max = length

        covered = covered | candidate
        result.append(candidate)
        F.remove(candidate)

    elapsed = (time.clock() - start)

    F_set = set()
    for i in result:
        F_set = F_set | i
    _check= X == F_set

    print("\n-------------------")
    print("Test greedy_set_cover Time used:%s, F'size:%s"%(elapsed,len(X)))
    print("C's size: %d \ncover all elements in X:%s" % (len(result), _check))

    return result


def LP_set_cover(X, F):
    start = time.clock()
    var_name = ["S" + str(x) for x in range(len(F))]
    lp = LpProblem("The Problem of set cover", LpMinimize)
    lp_vars = LpVariable.dicts("lp", var_name, lowBound=0, upBound=1, cat=LpContinuous)
    all_occur = []
    for x in X:
        occur = {}
        for index, f in enumerate(F):
            if x in f:
                occur["S" + str(index)] = 1
            else:
                occur["S" + str(index)] = 0
        all_occur.append(occur)

    C_S={}
    for x in range(len(F)):
        C_S["S" + str(x)]=len(F[x])
    lp += lpSum([lp_vars[i] for i in var_name])
    for occur in all_occur:
        lp += lpSum([occur[i] * lp_vars[i] for i in var_name]) >= 1
    solve_state=lp.solve()
    result = []
    max_count = max([sum(occur.values()) for occur in all_occur])

    for v in lp.variables():
        if v.varValue > (1.0/max_count):
            result.append(F[int(v.name[4:])])
    elapsed = (time.clock() - start)
    F_set = set()
    for i in result:
        F_set = F_set | i
    _check = X == F_set

    print("\n-------------------")
    print("Test LP_set_cover Time used:%s, F'size:%s"%(elapsed,len(X)))
    print("C's size: %d \ncover all elements in X:%s" % (len(result), _check))

    # print result
    # print F
    # print F_set



def plot(C, num):
    row_num = int(round(num ** 0.5) + 1)
    col_num = row_num
    image = np.zeros((row_num, col_num))
    image = image.reshape((-1))
    result = []
    for x in C: result += list(x)
    for x in result: image[x] += 1
    max_ = int(image.max())
    min_ = int(image.min())
    bar = np.zeros((1, max_ - min_ + 1))
    color = min_
    for i in range(max_ - min_ + 1):
        bar[0][i] = color
        color += 1
    image = image.reshape((row_num, col_num))
    plt.subplot(2, 1, 1)

    plt.imshow(image)
    plt.subplot(9, 1, 8)
    plt.imshow(bar)
    plt.show()


if __name__ == "__main__":

    nums = [64, 256, 512, 1024, 2048, 4096]
    # nums = [200]
    # nums = [10, 20, 30, 40, 50]

    threshold=30
    for num in nums:

        print 'Generate Data, nums of data:%s, threshold:%s'%(num, threshold)
        X, F = data_generator(num, threshold)

        result = greedy_set_cover(X, F)
        # plot(result, num)

        result = LP_set_cover(X, F)
        # plot(result, num)




    # plt.figure()
    # x = [i for i in range(len(times_greedy))]
    # plt.plot(x, times_greedy, 's-', color='red')
    # plt.plot(x, times_lp, 'o-', color='green')
    # plt.show()
