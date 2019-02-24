# num=raw_input()
num = 99999
# case1 90900 9wl9b
# case2 90909 9wl9bl9

arr = ['W', 'Q', 'B', 'S', 'L']

len = len(str(num))
res = ''

tmp = num
for i in range(len, 1, -1):
    if tmp / (pow(10, i)) != 0:
        res = res +  str(num)[len - i] + arr[len - i]
    elif tmp / (pow(10, i)) == 0 and str(num)[len - i + 1] != 'O':
        res = res + 'L'

    tmp = tmp % (pow(10, i))

if str(num)[-1] != 'O':
    res += str(num)[-1]

print res
# print len
# print list('abcde')
