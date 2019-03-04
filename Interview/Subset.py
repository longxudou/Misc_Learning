import operator

def subsets( nums):
    res = [[]]
    for num in sorted(nums):
        print res
        res += [item+[num] for item in res]
        print res
    return res


def subsets2(nums):
    res = []
    nums.sort()
    for i in xrange(1<<len(nums)): #2^nums
        tmp = []
        for j in xrange(len(nums)):
            print i & 1 << j, i,j, 1 << j
            if i & 1 << j:  # if i >> j & 1:
                tmp.append(nums[j])
            # print j
        #         print i,
        # print '\n'
        print tmp, i
        # res.append(tmp)
    return res

# subsets2([1,2,3])


# DFS recursively
def subsets1(self, nums):
    res = []
    self.dfs(sorted(nums), 0, [], res)
    return res


def dfs(self, nums, index, path, res):
    res.append(path)
    for i in xrange(index, len(nums)):
        self.dfs(nums, i + 1, path + [nums[i]], res)


# print reduce(operator.xor,[1,1,2,2,4])
for idx,char in enumerate('abc'):
    print idx,char