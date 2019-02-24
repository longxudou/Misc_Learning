M = []


def quick_sort(left, right):
    if (left > right):
        return

    temp = M[left]
    i = left
    j = right

    while (i != j):
        while (M[j] >= temp and i < j):  # from left to right to catch the little one, first
            j -= 1
        while (M[i] <= temp and i < j):
            i += 1

        if i < j:
            M[i], M[j] = M[j], M[i]  # swap

    M[left] = M[i]
    M[i] = temp

    quick_sort(left, i - 1)
    quick_sort(i + 1, right)


def quick_sort2(M):
    if len(M) < 2:
        return M
    else:
        baseValue = M[0]
        less, equal, greater = [], [baseValue], []
        for m in M:
            if m < baseValue:
                less.append(m)
            elif m > baseValue:
                greater.append(m)
            else:
                equal.append(m)
        return quick_sort2(less) + equal + quick_sort2(greater)


if __name__ == "__main__":
    M = [2, 3, 1, 5, 1, 0]
    # quick_sort2(M)
    quick_sort(0, len(M)-1)
    print M
