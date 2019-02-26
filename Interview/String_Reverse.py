def reverseString( s):
    """
    :type s: List[str]
    :rtype: None Do not return anything, modify s in-place instead.
    """
    # return "".join(reversed(list(s)))
    for i in range(len(s) // 2):
        s[i], s[-i - 1] = s[-i - 1], s[i]
    return s

print reverseString(["h","e","l","l","o"])

score={'a':2,'z':1,'x':3}

score= sorted(score.items(),key=lambda item:item[1],reverse=True)
print score
# print sorted(score.values())