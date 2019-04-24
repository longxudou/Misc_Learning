import random
import time
import sys

def quick_sort(M, left, right):
    if left < right:
        lt, gt = rand_partition(M, left, right)
        quick_sort(M, left, lt - 1)
        quick_sort(M, gt + 1, right)
    return

def rand_partition(M, left, right):
    i = random.randint(left, right)
    M[right], M[i]= M[i], M[right]
    pivot = M[left]
    lt = left
    i = left + 1
    gt = right

    while i<=gt:
        if M[i]<pivot:
            M[i],M[lt]=M[lt],M[i]
            lt=lt+1
            i=i+1
        elif M[i]>pivot:
            M[i], M[gt] = M[gt], M[i]
            gt=gt-1
        else:
            i+=1


    return lt,gt
    #M-> [less than pivot] [equal to pivot] [pivot] [greater than pivot]
    #lt -> the begin of [equal]
    #gt -> the end of [equal]

def test1():
    # 1,000,000 integer 32-bit
    start = time.clock()

    M1 = [random.randint(-(2 ** 32 - 1), 2 ** 32 - 1) for i in range(1000000)]
    _M1 = M1[:]
    quick_sort(M1, 0, len(M1) - 1)
    print M1 == sorted(_M1)

    elapsed = (time.clock() - start)
    print("Test 1 Time used:%s, %s"%(elapsed,'1,000,000 integer 32-bit'))

def test2():
    #1,000,000 integer 1
    start = time.clock()

    #1,000,000 1
    M2 = [1 for i in range(1000000)]
    _M2 = M2[:]
    quick_sort(M2, 0, len(M2) - 1)
    print M2==sorted(_M2)

    elapsed = (time.clock() - start)
    print("Test 2 Time used:%s, %s"%(elapsed,'1,000,000 integer 1'))

def test3(total_num, percentage):
    """

    :param total_num: the num of test case
    :param percentage: the percentage of 1 in test case
    :return:
    """
    start = time.clock()

    num_of_1 = int(total_num * percentage)
    num_of_int32 = total_num - num_of_1
    M3 = [1 for i in range(num_of_1)]
    M3 = M3 + [random.randint(-(2 ** 32 - 1), 2 ** 32 - 1) for i in range(num_of_int32)]
    _M3 = M3[:]
    quick_sort(M3, 0, len(M3) - 1)
    print M3 == sorted(_M3)

    elapsed = (time.clock() - start)
    print("Test 3 Time used:%s, total num:%s, percentage:%s"%(elapsed,total_num, percentage))

if __name__ == "__main__":
    # test1()
    # test2()

    for total_num in [10000,1000,5000]:
        for percentage in [0.5,0.6,0.7,0.8,0.9,1.0]:
            test3(total_num,percentage)

    # M=[7,1,2,5,4,4]
    # quick_sort(M,0,len(M)-1)
    # print M