import re,json,os, argparse

TIME_INTERVAL=30

def divide(path):
    with open(path, 'r') as f:
        lines=f.readlines()

    new_lines=[]
    for i in lines:
        if i!='\n':
            new_lines.append(i.strip())
    lines=new_lines

    sent_cnt=len(lines)//5

    collect=[]
    tmp=[]
    for index in range(sent_cnt):
        start=int(lines[index*3+1][6:8])
        end=int(lines[index*3+1][23:25])
        sentence=lines[index*3+2]

        print(start,end)

        # 0, start, end , 30
        if 0<start<=end<30:
            if index==0 or int(lines[index*3-2][23:25])<30:
                tmp.append(sentence)
            else:
                collect.append(tmp)
                tmp=[sentence]

        # 0, start, 30, end
        elif 0<start<30<end:
            tmp.append(sentence)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, 0, end
        elif 30<start and 0<end<30:
            tmp.append(sentence)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, end
        elif 30<start<=end:
            if index == 0 or int(lines[index * 3 - 2][6:8]) > 30:
                tmp.append(sentence)
            else:
                collect.append(tmp)
                tmp=[sentence]


    if tmp!=[]:
        collect.append(tmp)
    return collect


if __name__ == '__main__':
    path_list=['/Users/longxud/Downloads/time/2020-03-10.srt']
    for file_path in path_list:
        collect=divide(file_path)
