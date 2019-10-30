# ans={}
# thres=10
#
# for i in range(1,thres):
#     for j in range(i+1,thres):
#         for k in range (j+1,thres):
#             ans[(i,j,k)]=i*j*k
#
# # ans=list(set(sorted(ans)))
# ans =  sorted(ans.items(), key=lambda d: d[1])
#
#
# with open('multi.txt','w') as f:
#     for key, value in ans:
#         f.write(','.join(map(str, key))+'->'+str(value)+'\n')


ans={}
thres=10

for i in range(1,thres):
    for j in range(i+1,thres):
        for k in range (j+1,thres):
            for m in range(k+1,thres):
                ans[(i,j,k,m)]=i*j*k*m

# ans=list(set(sorted(ans)))
ans =  sorted(ans.items(), key=lambda d: d[1])

print ans

with open('multi2.txt','w') as f2:
    for key, value in ans:
        f2.write(','.join(map(str, key))+'->'+str(value)+'\n')