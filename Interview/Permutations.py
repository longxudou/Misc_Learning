class Solution(object):
    def permute(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        self.ans = []
        # self.dfs(nums, [])
        self.dfs2(nums, 0)
        return self.ans

    def dfs(self, nums, path):
        if not nums:
            self.ans.append(path)
        for i in range(len(nums)):
            self.dfs(nums[:i] + nums[i + 1:], path + [nums[i]])

    def dfs2(self, nums, idx):
        print idx,nums
        if idx == len(nums) - 1:
            self.ans.append(nums[:])
        else:
            for i in range(idx, len(nums)):
                nums[idx], nums[i] = nums[i], nums[idx]
                self.dfs2(nums, idx+1)
                nums[idx], nums[i] = nums[i], nums[idx]


def main():
    ret = Solution().permute([1, 2, 3])

    print ret


if __name__ == '__main__':
    main()
