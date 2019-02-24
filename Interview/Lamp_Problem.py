light_num=1000
person_num=65535

light=[0 for i in range(light_num)]
ans=0


for i in range(1, person_num):
    if i*i>person_num:
        break
    ans+=1
# x=raw_input()
# print len(light)
print ans