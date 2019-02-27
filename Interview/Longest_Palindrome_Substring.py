import numpy as np


class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        if len(s)==0:
            return s

        dp = [[0 for i in range(len(s))] for j in range(len(s))]

        # init
        for i in range(len(s) - 1):
            dp[i][i] = 1
            if s[i] == s[i + 1]:
                dp[i][i + 1] = 1
        dp[-1][-1] = 1

        seq_len = 0

        for seq_len in range(2, len(s) + 1):
            for i in range(len(s) - seq_len + 1):
                if s[i] == s[i + seq_len - 1] and dp[i + 1][i + seq_len - 2] == 1:
                    dp[i][i + seq_len - 1] = 1

        print  np.array(dp)
        #     # "abcba"
        _max = 0
        _i = 0
        _j = 0
        for i in range(len(s)):
            for j in range(i, len(s)):
                if dp[i][j] and j - i > _max:
                    _max = j - i
                    _i = i
                    _j = j
        return s[_i:_j+1]



def stringToString(input):
    return input[:].decode('string_escape')


def main():
    s = stringToString("cbbd")

    ret = Solution().longestPalindrome(s)

    out = (ret)
    print out


if __name__ == '__main__':
    main()
