import re,json,os, argparse
from collections import Counter
from api import query
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

        # print(start,end)

        # 0, start, end , 30
        if 0<start<=end<TIME_INTERVAL:
            if index==0 or int(lines[index*3-2][23:25])<TIME_INTERVAL:
                tmp.append(sentence)
            else:
                collect.append(tmp)
                tmp=[sentence]

        # 0, start, 30, end
        elif 0<start<TIME_INTERVAL<end:
            tmp.append(sentence)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, 0, end
        elif TIME_INTERVAL<start and 0<end<TIME_INTERVAL:
            tmp.append(sentence)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, end
        elif TIME_INTERVAL<start<=end:
            if index == 0 or int(lines[index * 3 - 2][6:8]) > TIME_INTERVAL:
                tmp.append(sentence)
            else:
                collect.append(tmp)
                tmp=[sentence]

    if tmp!=[]:
        collect.append(tmp)
    return collect

def set_tag_for_interval(list_of_interval):
    result = []
    for list_of_sentence in list_of_interval[:2]:
        per_sentence_tag=query(list_of_sentence)
        tag_frequence=Counter([i['name'] for i in per_sentence_tag['results']])
        result.append(tag_frequence.most_common(1)[0][0])


    return result

if __name__ == '__main__':
    path_list=['/Users/longxud/Downloads/time/2020-03-10.srt']
    for file_path in path_list:
        collect=divide(file_path)
        result=set_tag_for_interval(collect)
        print(result)
