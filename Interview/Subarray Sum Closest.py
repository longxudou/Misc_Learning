import sys
from math import *

class Solution:
    """
    @param: nums: A list of integers
    @return: A list of integers includes the index of the first number and the index of the last number
    """

    def subarraySumClosest(self, nums):
        # write your code here
        sums = {}
        _sum = 0
        for idx in range(len(nums)):
            _sum += nums[idx]
            sums[idx] = _sum

        sorted_sumOfprefix = sorted(sums.items(), key=lambda element: element[1])

        print sorted_sumOfprefix

        right=0
        left=0
        min_difference=sys.maxint

        for i in range(1, len(sorted_sumOfprefix)):
            former_element=sorted_sumOfprefix[i-1]
            later_element=sorted_sumOfprefix[i]
            
            if abs(former_element[-1]-later_element[-1])<min_difference:
                right=max(former_element[0],later_element[0])
                left=min(former_element[0],later_element[0])+1
                min_difference=abs(former_element[-1]-later_element[-1])
                print right,left,min_difference,former_element[-1],later_element[-1]
        return [left,right]

print Solution().subarraySumClosest([-3, 1, 1, -3, 5])

