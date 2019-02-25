def maxAbs(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    length = len(nums)

    max_ = nums[:]
    min_ = nums[:]
    ans = 0

    for i in range(1, length):
        max_[i] = max(max_[i - 1] + nums[i], nums[i])
        min_[i] = min(min_[i - 1] + nums[i], nums[i])

        ans = max(ans, abs(max_[i]), abs(min_[i]))
        print ans
    print max_
    print min_
    return ans


print maxAbs([1,-3,2,-1])