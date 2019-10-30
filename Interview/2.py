from math import *

def solve(input):
    n, xc, yc , r = map(int, input.split(' '))
    def cover(grid):
        for point in grid:
            if sqrt(pow(point[0] - xc, 2) + pow(point[1] - yc, 2)) > r:
                return False
        return True

    grid_dict={}
    for i in range(n):
        for j in range(n):
            grid_1=(i,j)
            grid_2=(i+1,j)
            grid_3=(i,j+1)
            grid_4=(i+1,j+1)
            grid_dict[(i+1)+4*j]=[grid_1,grid_2,grid_3,grid_4]

    ans=[]
    for i in grid_dict.keys():
        if cover(grid_dict[i]):
            continue

        for point in grid_dict[i]:
            if sqrt(pow(point[0]-xc,2)+pow(point[1]-yc,2))<r:
                print(str(i),point)
                ans.append(str(i))
                break
    if ans==[]:
        print('-1')
    else:
        print(' '.join(ans))

def main():
    # input=raw_input()
    input='4 3 2 2'
    solve(input)

if __name__ == '__main__':
    main()