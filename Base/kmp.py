next = {}

def getNext(p):
    next[0] = -1
    i = 0
    j = -1
    while (i < len(p)):
        if (j == -1 or p[i] == p[j]):
            i = i + 1
            j = j + 1
            next[i] = j
            print 'i:',i,'--next[i]:',next[i],'---str:',
        else:
            j = next[j]

def kmp(string_text, pattern_text):
    i = 0
    j = 0

    while (i < len(string_text) and j < len(pattern_text)):
        if (j == -1 or string_text[i] == pattern_text[j]):
            i = i + 1
            j = j + 1
        else:
            j = next[j]

    if j == len(pattern_text):
        return i - j
    else:
        return -1


if __name__ == "__main__":
    string_text = 'ababababca'
    pattern_text = 'abababca'
    getNext(pattern_text)
    print next
    # print kmp(string_text,pattern_text)
