import bilibili_api
from wordcloud import WordCloud
import csv
import os
import time, random


# total = 1  # data1中的行数


def main(total=1):
    with open('Infor_Recommendation/data1.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        i = 0
        for item in reader:
            if i <= total:
                i = i + 1  # 第一行不要
                continue
            try:
                user_uid = item[0]
                up_uid = item[1]
                bvid = func_video_info(up_uid)
                suc = func_video_tag(user_uid, up_uid, bvid)
                if suc:
                    total = total + 1
                    print("————————看这里————————————")
                    print(str(total)+"行")
                    # time.sleep(random.random() * 3)
                else:
                    print("定位3————结束了————")
                    print(total)
                    break
            except Exception as e:
                print(e)
                time.sleep(30)
                main(total)
                break

        f.close()


def func_video_tag(user_uid, up_uid, bvid):
    '''
    根据视频bvid获得对应视频标签，并在此函数中进行数据整合和数据集生成
    :param user_uid:用户uid
    :param up_uid:被关注up主uid
    :param bvid:up主发布视频的bvid
    :return:
    '''
    print("——————在爬取tag————————")
    fail = 0
    for item in bvid:
        count1 = 0
        count1 = count1 + 1
        try:
            time.sleep(random.random()*3)
            tag_l = bilibili_api.video.get_tags(item)
            count = 0
            for l in tag_l:
                # tag_sum.append(l['tag_name'])
                count = count + 1
                # print(l['tag_name'])
                temp = [user_uid, up_uid, l['tag_name']]
                with open('tag_data_100.csv', 'a', newline='', encoding='utf-8')as f:
                    f_csv = csv.writer(f)
                    # f_csv.writerow(headers)
                    f_csv.writerow(temp)
                    f.close()
                #if count == 2:
                 #   break
        except Exception as e:
            print('定位2\n————爬取tag失败————')
            print(e)
            print(count1)
            #fail = fail + 1
            time.sleep(random.random()*600)
            continue
    return True


def func_video_info(uid):
    # 只读前10条视频的bvid
    r_video = bilibili_api.user.get_videos(int(uid))
    # print(r_video)
    # print(type(r_video))
    # test_txt(r_video)
    bvid_list = []
    count = 0
    for item in r_video:
        bvid_list.append(item['bvid'])
        count = count + 1
        if (count == 100):
            break
    # print(str(uid) + '共发布了' + str(len(list1)) + '条视频')
    print("定位1————爬取bvid————")
    print(str(len(bvid_list)))
    return bvid_list

'''
def fun_save(file_name, list1):
    file = open(file_name, mode='w', encoding='utf-8')
    for i in range(len(list1)):
        line = str(list1[i]).replace(',', '\n').replace('[', '').replace(']', '') + '\n\n'
        file.write(line)
    file.close()
'''
if __name__ == '__main__':
    if not os.path.exists("tag_data_100.csv"):
        with open('tag_data_100.csv', 'w', newline='', encoding='utf-8')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(['user', 'up_as_item', 'tag'])
            f.close()
    total = input("上一次读到多少行了？")
    main(int(total) + 1)
# 75330
