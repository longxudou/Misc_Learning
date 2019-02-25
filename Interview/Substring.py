
def maxSubArray( nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    if nums == []:
        return 0

    # transition function: f(i)=max{f(i-1_+x[i],x[i]}

    # solution 1: o(n), dp
    #         f=[0 for i in range(len(nums))]

    #         f[0]=nums[0]
    #         for index in range(1, len(nums)):
    #             f[index]=max(f[index-1]+nums[index], nums[index])

    #         return max(f)

    # solution2 : o(nlogn), divide and conquer

    return maxSubArrayDivide(nums, 0, len(nums)-1)


def maxSubArrayDivide(nums, left, right):
    print left,right

    if left >= right:
        # if left<len(nums):
        #     return nums[left]
        # else:
        #     return 0
        return nums[left]
        # try:
        #     return nums[left]
        # except:
        #     print len(nums), left
        #     return 1

    mid = (left + right) / 2
    lmax = maxSubArrayDivide(nums, left, mid)
    rmax = maxSubArrayDivide(nums, mid + 1, right)
    mmax = nums[mid]

    tmp = mmax
    for i in range(mid - 1,left-1, -1):
        tmp += nums[i]
        mmax = max(mmax, tmp)
        print 'tmp',tmp

    print mid, mmax

    tmp = mmax
    for i in range(mid + 1, right+1, 1):
        tmp += nums[i]
        mmax = max(mmax, tmp)

    print mid,mmax

    return max(lmax, max(mmax, rmax))

l=[1,2]
print maxSubArray(l)