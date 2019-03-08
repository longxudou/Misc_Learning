import re
import sys


class Solution(object):
    def myAtoi(self, str):
        """
        :type str: str
        :rtype: int
        """
        str = str.strip()
        # str = re.findall(r'(^[+-0]*\d+)\D*$',str)
        str = re.findall('(^[\+\-0]*\d+)\D*', str)

        try:
            MAX_INT = 2147483647
            MIN_INT = -2147483648

            print str
            result = int(str[0])
            # result = int(''.join(str))
            if result > MAX_INT > 0:
                return MAX_INT
            elif result < MIN_INT < 0:
                return MIN_INT
            else:
                return result

        except:
            return 0


def stringToString(input):
    return input[1:-1].decode('string_escape')


def intToString(input):
    if input is None:
        input = 0
    return str(input)


def main():

    ret = Solution().myAtoi('-91283472332')

    out = intToString(ret)
    print out



if __name__ == '__main__':
    main()