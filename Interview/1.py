import re

def solve(input):
    res = {}
    def _split(input, i=0, is_array=False):
        if i not in res:
            res[i] = []
        if i+1 not in res:
            res[i+1] = []

        is_current = False
        for element in input:
            if isinstance(element, str):
                if is_array:
                    if is_current:
                        res[i+1][-1].append(element)
                    else:
                        res[i+1].append([element])
                        is_current = True
                else:
                    res[i].append(element)
            else:
                _split(element, is_array=True)

    input=re.sub('(\w+)', lambda x: "'" + x.group(1) + "'", input)
    input=eval(input)
    _split(input)
    indices = res.keys()
    min_index, max_index = min(indices), max(indices)
    for i in range(max_index, min_index-1, -1):
        if res[i] and isinstance(res[i][0], list):
            res[i] = str(res[i])[1:-1]
        print (re.sub(r'\'(\w+)\'', lambda x: x.group(1), str(res[i])))

def main():
    input=raw_input()
    # input='[[tshirt],[doll],toy,apple]'
    # input='[[apple]]'
    # input = '[[tshirt,doll],toy,apple]'
    solve(input)

if __name__ == '__main__':
    main()