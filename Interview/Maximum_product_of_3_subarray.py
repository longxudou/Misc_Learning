def maximumProduct(nums):
    """
    :type nums: List[int]
    :rtype: int
    """

    ans=nums[0] * nums[1] * nums[2]

    for i in range(1, len(nums)-1):
        ans = max(nums[i - 1] * nums[i] * nums[i + 1],ans)
        
    return ans


print maximumProduct([1,2,3,4])