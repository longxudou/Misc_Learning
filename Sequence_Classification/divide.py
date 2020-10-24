import re,json,os, argparse
import time, xlrd, xlsxwriter
from datetime import datetime
from collections import Counter
from Sequence_Classification.api import query, get_access_token
TIME_INTERVAL=30

access_token = get_access_token()

class item():
    def __init__(self,start_time,end_time,content):
        self.start_time=start_time
        self.end_time=end_time
        self.content=content

    def __repr__(self):
        # return f"{self.start_time.tm_hour}:{self.start_time.tm_min}:{self.start_time.tm_sec}-{self.end_time.tm_hour}:{self.end_time.tm_min}:{self.end_time.tm_sec}-{self.content}"

        return f"{self.start_time.tm_min}:{self.start_time.tm_sec}-{self.end_time.tm_min}:{self.end_time.tm_sec}-{self.content}"

def divide(path):
    with open(path, 'r') as f:
        lines=f.readlines()

    new_lines=[]
    for i in lines:
        if i!='\n':
            new_lines.append(i.strip())
    lines=new_lines

    sent_cnt=len(lines)//3

    item_list=[]
    for index in range(sent_cnt):
        start=lines[index*3+1][0:8]
        end=lines[index*3+1][17:25]

        start=time.strptime(start, "%H:%M:%S")
        end = time.strptime(end, "%H:%M:%S")

        sentence=lines[index*3+2]
        item_list.append(item(start,end,sentence))

    collect=[]
    tmp=[]
    for index in range(sent_cnt):
        cur_item = item_list[index]
        start=cur_item.start_time.tm_sec
        end=cur_item.end_time.tm_sec
        sentence=cur_item.content

        # 0, start, end , 30
        if 0<=start<=end<=TIME_INTERVAL:
            # if tmp != [] and item_list[index-1].start_time.tm_min!=cur_item.start_time.tm_min:
            if tmp != [] and item_list[index - 1].start_time.tm_sec > TIME_INTERVAL:
                collect.append(tmp)
                tmp = [cur_item]
            else:
                tmp.append(cur_item)

        # 0, start, 30, end
        elif 0<=start<=TIME_INTERVAL<end:
            tmp.append(cur_item)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, 0, end
        elif TIME_INTERVAL<=start and 0<=end<TIME_INTERVAL:
            tmp.append(cur_item)
            collect.append(tmp)
            tmp=[]

        # 0, 30, start, end
        elif TIME_INTERVAL<=start<=end:
            if tmp != [] and item_list[index-1].start_time.tm_sec<TIME_INTERVAL:
                collect.append(tmp)
                tmp = [cur_item]
            else:
                tmp.append(cur_item)


    if tmp!=[]:
        collect.append(tmp)
    return collect

def set_tag_for_interval(list_of_interval):
    result = []
    tag_list=[]

    for list_of_sentence in list_of_interval:
        per_sentence_tag=query([i.content for i in list_of_sentence], access_token)
        tag_frequence=Counter([i[0] for i in per_sentence_tag])
        tag_list.append(tag_frequence.most_common(1)[0][0])

    cnt=0
    for tag, interval in zip(tag_list,list_of_interval):
        interval_start=f"{interval[0].start_time.tm_hour}:{interval[0].start_time.tm_min}:{interval[0].start_time.tm_sec}"
        interval_end = f"{interval[-1].start_time.tm_hour}:{interval[-1].start_time.tm_min}:{interval[-1].start_time.tm_sec}"

        interval_content = ''.join([i.content for i in interval])
        result.append((f'{cnt}-{cnt+len(interval)-1}',interval_start,interval_end,interval_content,tag))
        cnt = cnt+len(interval)

    return result

def write_xls(result):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('sample.xlsx')
    worksheet = workbook.add_worksheet()

    #('5-6', '0:0:31', '0:0:43', '啊。啊。', 'teach')
    # Write some data headers.
    worksheet.write('A1', 'Index')
    worksheet.write('B1', 'Start')
    worksheet.write('C1', 'End')
    worksheet.write('D1', 'Text')
    worksheet.write('E1', 'Tag')

    # Start from the first cell below the headers.
    row = 1
    col = 0

    for Index, Start, End, Text, Tag in (result):
        # Convert the date string into a datetime object.
        worksheet.write_string(row, col, Index)
        worksheet.write_string(row, col + 1, Start)
        worksheet.write_string(row, col + 2, End)
        worksheet.write_string(row, col + 3, Text)
        worksheet.write_string(row, col + 4, Tag)
        row += 1
    workbook.close()

def merge_interval_based_on_tag(interval_list):
    result=[]
    tmp=[interval_list[0]]
    for interval in interval_list[1:]:
        if interval[-1]==tmp[-1][-1]:
            tmp.append(interval)
        else:
            merge_interval = (f'{tmp[0][0].split("-")[0]}-{tmp[-1][0].split("-")[1]}',
                              tmp[0][1],
                              tmp[-1][2],
                              ''.join([i[3] for i in tmp]),
                              tmp[0][-1])
            result.append(merge_interval)
            tmp=[interval]
    if tmp!=[]:
        merge_interval = (f'{tmp[0][0].split("-")[0]}-{tmp[-1][0].split("-")[1]}',
                          tmp[0][1],
                          tmp[-1][2],
                          ''.join([i[3] for i in tmp]),
                          tmp[0][-1])
        result.append(merge_interval)
    return result

if __name__ == '__main__':
    path_list=['/Users/longxud/Downloads/time/2020-03-10.srt']
    for file_path in path_list:
        list_of_interval=divide(file_path)
        result=set_tag_for_interval(list_of_interval[:5])
        print(result)
        merge_interval_based_on_tag(result)
        write_xls(result)

        # test=[('0-4', '0:0:13', '0:0:25', '各位同学，请通知一下其他同学是吧？抓紧时间，我们进入腾讯会议系统。嗯。不好。啊。', 'QAcommunication'),
        #       ('5-6', '0:0:31', '0:0:43', '啊。啊。', 'teach'),
        #       ('7-10', '0:1:14', '0:1:20', '嗯。啊。酷狗。嗯。', 'other'),
        #       ('11-14', '0:1:35', '0:1:44', '再进来邀请一下其他人啊其他同学。嗯。我们几位助教是吧，抓紧时间督促一下。我们再稍等几分钟啊。', 'QAcommunication'),
        #       ('15-22', '0:2:8', '0:3:29', '啊。啊。可以吗？嗯。啊。嗯。嗯。啊。', 'teach'),
        #       ('23-30', '0:3:31', '0:3:59', '我靠。我这还得扣记一记。哈哈哈。怎么样？哎，这回交这回行了，挺好的啊，挺好听啦。哎，好好。各位同学能听到声音吗？如果听到声音的话，可以在。', 'QAcommunication'),
        #       ('31-38', '0:4:1', '0:4:25', '我们这个聊天儿里头或者在q q 群里回复啊。很好很好啊。很好。嗯。好好。我们现在进来了，还缺一些人。呃，各位同学啊，那我们就开始上课啊。我想的话呢呃请各位同学啊记住我们上课的这样一个纪律啊，也就是我们上课之前先宣布纪律啊。', 'QAcommunication'),
        #       ('39-44', '0:4:36', '0:4:56', '我们这门课呀应该说学起来不是很难啊，考试也不是很难，但是需要你深入的学啊。那但是呢课是必须要加。那如果说我们。啊，我们呢下一步就是在。超级学习通里面来这个呃。签到来这个讨论啊，有些讨论话我们还是在这个超级学习中里头。', 'teach'),
        #       ('45-48', '0:5:3', '0:5:27', '那我们这个呃课堂呢，我们是用腾讯会议啊用腾讯会议。所以我想呢这一点呢各位同学是要这是第一个来讲。那么第二个来讲呢，就是我们如果说我们这门课是吧呃，在统计我们的出勤率方面是吧。如果说你去三课。啊，我们就直接就没有成绩了。啊，这一点我们先说这个纪律啊先说纪律。那么偶尔缺一次呢两次啊，这个我觉得是可以的，可以理解。', 'teach'),
        #       ('49-53', '0:5:35', '0:5:51', '但是如果是你缺席了3次及以上。那这门课的成绩就自动就没有了啊。我想我们各位同学一定要注意。因为我们呢这里面就是以我们的这个签到数据为准。也就是我们超级学习通。啊，也就是所有同学都要进入超级学习中来做，这是我们宣布的这样一个纪律啊，宣布这样一个纪律啊。', 'teach'),
        #       ('54-60', '0:6:0', '0:6:27', '那我们呢用这个。腾讯会议是吧，那大家可以看到是吧，我们在这里面呢，我给大家先看我们的这种课程的基本要求啊，课程的基本要求啊。那也就是说。这个文件呢我们已经下发了。保密已经下发了。哦，我找到啊，稍等一下。嗯，好嘞。', 'teach'),
        #       ('61-65', '0:6:34', '0:6:50', '哎呀，我把这个文档打开。这个不是苹果。可从表面这个要求。嗯。啊。', 'teach'), ('66-71', '0:7:3', '0:7:25', '我们同学能看到吧。嗯。是不是能看到我这个p p a 这个文档，如果能的话，在这个群聊里头是吧，来回答好。妈的。啊。那我们这门课呢叫企业资源规划与供电管理系统啊。', 'other'),
        #       ('72-74', '0:7:31', '0:7:52', '我们是三上学时16次课啊，两个学分。所以这个呢大家是要知道。那我们的这种教学方式呢，大家看就是这个图啊，这个图啊，那我们说一方面我们以q q 群为q q 群为中心，q q 群，微信群啊，我们在及时通知。啊，所有通知我想我们同学都要关注这个q q 群啊，这是这是一个。第二个来讲呢，我们会有这种啊语音直播啊啊这是在这里面，也就是我们来给大家上课啊。那么因为我们这门课呢，在spoke 里面已经给大家提供了视频了啊，提供了视频了。', 'teach'),
        #       ('75-77', '0:8:12', '0:8:21', '课的时候呢会给大家做一些重点的讲解。我们不会按照这个视频来讲解。但是因为我们说。我们这门课啊是偏管理和计算机相结合的，这样一个课有点偏管理。所以很强调同学对这里面内容的理解。', 'teach'),
        #       ('78-80', '0:8:31', '0:8:55', '那因此我这个课堂呢会主要的啊来做一些这种啊同学对于我们这个问题的这种理解方面的这种讨论。所以这一点很重要，因为什么呢？因为我们说啊管理啊，什么是管理啊，那如果我们自己没有体会的话，管理类的课来讲，学了等于白学啊，我们听一遍就完了。所以我们一定要深刻的这样一个体验，要自我去思考，只有自我去扫，我们才能够啊掌握这种管理的这样一些技巧啊，掌握管理这样一些技巧。所以我想这一点呢，我们各位同学是要注意啊，各位注意一点啊。所以强化我们这样一个理解。', 'teach'),
        #       ('81-82', '0:9:12', '0:9:16', '那我们这个教学日历呢在这里面已经给大家列出来了。啊，那我们的后边的视频呢会提前一周啊给大家发布啊，我们现在发布的是第一讲和第二讲啊，我相信同学已经看到了啊，那如果没有看到的抓紧时间联系是吧，我们是放在了这个超行学习通这个平台上了啊，超行学习通平台是吧。所以我们在课程资料都在。', 'teach'),
        #       ('83-85', '0:9:36', '0:9:44', '台上啊，所以我想这个同学是要理解啊。那另外一个就是我们的这种学习。啊，我们一方面是线上资源啊，就是我们这个smoke 是吧，我们有大约是16家啊，在16家呢，因为我们说不是说很均衡啊，不是说很均衡。有的有的讲的有一些。', 'teach'),
        #       ('86-88', '0:10:0', '0:10:21', '可能是两个小时左右的视频，有一些讲的大概是一个小时左右，这个也就是五六十分钟啊。那有一些讲的比较关键，那就是这种。啊，120分钟左右，130分钟大于这样的一个情况。但是这些视频呢，我们说同学你可以啊，如果说你感觉你学的好，你完全可以是1.5倍速来看。那1.5倍数来看的话呢啊那关键一点就是你能不能够思维跟得上啊，如果思维跟得上应该没有问题，那应该没有问题。所以说虽然是130分钟120分钟，但如果说你1.5倍速的话，大概也就是60分钟到70分钟就可以看完了啊。所以在这里面啊那。', 'teach'),
        #       ('89-91', '0:10:41', '0:10:56', '思考啊，那还有就是我们spoke 里面呢有一些这种作业啊，有一些作业啊，所以这地方呢将来我们会陆陆续续的发布给大家。那我们这种课堂学习。啊，我们课堂学习，所以课堂学习呢呃将来我们说现在是在线啊，将来我们实体课堂也是这样一种形式啊，也是这样一种形式是吧。那么实体课堂呢，我们更多的是啊也是要去交流啊，也是要去交流。所以我现在呢用腾讯会议是吧，跟我们实体课堂应该说没有什么差别。', 'teach')]
        # merge_interval_based_on_tag(test)
