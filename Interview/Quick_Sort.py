M = []


def quick_sort(left, right):
    if (left > right):
        return

    temp = M[right]
    # temp = M[left]
    i = left
    j = right

    while (i != j):
        while (M[i] <= temp and i < j):
            i += 1

        while (M[j] >= temp and i < j):  # from right to catch the little one, first
            j -= 1
        # while (M[i] <= temp and i < j):
        #     i += 1

        if i < j:
            M[i], M[j] = M[j], M[i]  # swap

    M[right] = M[i]
    # M[left]=M[i]
    M[i] = temp
    print left, right, i, j, M


    quick_sort(left, i - 1)
    quick_sort(i + 1, right)


def quick_sort2(M):
    if len(M) < 2:
        return M
    else:
        baseValue = M[0]
        less, equal, greater = [], [baseValue], []
        for m in M[1:]:
            if m < baseValue:
                less.append(m)
            elif m > baseValue:
                greater.append(m)
            else:
                equal.append(m)
        return quick_sort2(less) + equal + quick_sort2(greater)


def quick_sort_own(left, right):
    if left > right:
        return

    i, j = left, right
    tmp = M[left]

    while (i != j):
        if M[j] >= tmp and i < j:
            j -= 1
        if M[i] <= tmp and i < j:
            i += 1
        if i < j:
            M[i], M[j] = M[j], M[i]

    M[j], M[left] = M[left], M[j]

    quick_sort_own(left, i - 1)
    quick_sort_own(i + 1, right)


if __name__ == "__main__":
    M = [2, 3, 1, 5, 1, 0]
    # print quick_sort2(M)
    print M
    quick_sort(0, len(M)-1)
    # quick_sort_own(0, len(M) - 1)
    print M
