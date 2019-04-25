import random
import matplotlib.pyplot as plt
import numpy as np
from pulp import LpMinimize, lpSum, LpVariable, LpProblem, LpStatus, LpContinuous, value
import time


def data_generator(num):
    X = set()
    F = []

    for i in range(num):
        X.add(i)

    selected_index = []

    s0_index = [random.randint(0, num - 1) for _ in range(20)]
    F.append(set(s0_index))
    selected_index += s0_index
    while True:
        if num - len(selected_index) < 20:
            new_index = set([i for i in range(num)]) - set(selected_index)
            F.append(new_index)
            break
        size = random.randint(1, 20)
        new_ele_num = random.randint(1, size)
        new_index = []
        while new_ele_num > 0:
            tmp = random.randint(0, num - 1)
            if tmp not in selected_index:
                new_index.append(tmp)
                new_ele_num -= 1
        random.shuffle(selected_index)
        new_index += selected_index[:size - new_ele_num]
        F.append(set(new_index))
        selected_index += new_index

    while len(F) != num:
        new_index = []
        size = random.randint(1, int(num / 2))
        for i in range(size):
            new_index.append(random.randint(0, num - 1))
        F.append(set(new_index))
    return X, F


def greedy_set_cover(X, F):
    result = []
    covered = set()
    while len(covered) != len(X):
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
    return result


def LP_set_cover(X, F):
    var_name = ["S" + str(x) for x in range(len(F))]
    lp = LpProblem("The Problem", LpMinimize)

    lp_vars = LpVariable.dicts("lp", var_name, lowBound=0, upBound=1, cat=LpContinuous)

    lp += lpSum([lp_vars[i] for i in var_name])

    all_occur = []
    for x in X:
        occur = {}
        for index, f in enumerate(F):
            if x in f:
                occur["S" + str(index)] = 1.0
            else:
                occur["S" + str(index)] = 0.0
        all_occur.append(occur)

    for occur in all_occur:
        lp += lpSum([occur[i] * lp_vars[i] for i in var_name]) >= 1.0

    lp.solve()
    print("Status:", LpStatus[lp.status])
    print(value(lp.objective))
    result = []
    max_count = max([sum(occur.values()) for occur in all_occur])

    for v, f in zip(lp.variables(), F):
        # print(v.name, "=", v.varValue)
        if v.varValue > 1 / max_count:
            result.append(f)

    return result


def plot(C, num):
    row_num = round(num ** 0.5) + 1
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

    # nums = [64, 256, 512, 1024, 2048, 4096]
    nums = [10]
    # nums = [10, 20, 30, 40, 50]
    times_greedy = []
    times_lp = []
    for num in nums:
        X, F = data_generator(num)
        start = time.time()
        result = greedy_set_cover(X, F)
        end = time.time()
        times_greedy.append(round(end - start, 3))
        plot(result, num)
        print('count using greedy: %d' % len(result))
        start = time.time()
        result = LP_set_cover(X, F)
        end = time.time()
        times_lp.append(round(end - start, 3))
        plot(result, num)
        print('count using lp: %d' % len(result))

    plt.figure()

    x = [i for i in range(len(times_greedy))]
    print(times_greedy)

    plt.plot(x, times_greedy, 's-', color='red')
    plt.plot(x, times_lp, 'o-', color='green')
    plt.show()



