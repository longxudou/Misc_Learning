class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        l=s.split()

        ans=[]
        for word in l:
            ans.append(word[::-1])

        return ' '.join(ans)

        print ans


        # return 'a   '

def main():

    ret = Solution().reverseWords("Let's take LeetCode contest")

    print ret


if __name__ == '__main__':
    main()