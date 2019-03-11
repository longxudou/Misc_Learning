class Solution(object):
    def multiply(self, num1, num2):
        """
        :type num1: str
        :type num2: str
        :rtype: str
        """
        if num1=='0' or num2=='0':
            return '0'

        ans = ['0'] * (len(num1) + len(num2))

        for i in range(len(num1) - 1, -1, -1):
            carry = 0
            for j in range(len(num2) - 1, -1, -1):
                # tmp=ans[i+j+1]-'0'+(nums1[i]-'0')*(nums2[i]-'0')+carry
                tmp = int(ans[i + j + 1]) + int(num1[i]) * int(num2[j]) + carry
                ans[i + j + 1] = tmp % 10
                carry = tmp / 10
                # print ans,tmp,int(num1[i])*int(num2[i])
            ans[i] = int(ans[i]) + carry

        for i in range(len(ans)):
            ans[i] = str(ans[i])


        while (ans[0] == '0'):
            ans.pop(0)

        return ''.join(ans)


def stringToString(input):
    return input[1:-1].decode('string_escape')


def main():
    import sys


    ret = Solution().multiply('9899', '0')

    out = (ret)
    print out


if __name__ == '__main__':
    main()