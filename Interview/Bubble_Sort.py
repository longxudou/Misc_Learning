
M=[]

def bubble_sort(nums):
    for i in range(nums):
        for j in range(i, nums-1):
            if M[i]>M[j]:
                M[i], M[j]= M[j], M[i]


if __name__=="__main__":
    M=[2,3,5,1,0]
    bubble_sort(5)
    print M