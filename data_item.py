import csv
import bilibili_api
import requests
import json
import os
import time

# 我想爬数据集for 物品协同
'''
这个函数是用来爬虫的，与之有关的文件是
baida.csv 存储百大up的uid
data1.csv  存储爬取的信息
already_list.csv 存储已经爬过的uid

'''
num = 0
umid = []  # 记录爬过的uid


def main():
    # get_rookie_list() 之后还要写（新人榜单会更新），但是目前累了
    global umid  # 记录爬过的uid
    data_num = 200000
    # 数据集放在data1中
    if not os.path.exists("Infor_Recommendation/user_item.csv"):
        creat_csv()
    # 已经爬过的up信息放在already_list
    if not os.path.exists("already_list.csv"):
        with open('already_list.csv', 'w', newline='', encoding='utf-8')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(['uid'])
            f.close()
    # 读取已经爬过的up主列表
    with open('already_list.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        i = 0
        for item in reader:
            if i == 0:
                i = 1  # 第一行不要
                continue
            try:
                umid.append(item[0])
            except Exception as e:
                print(e)
        f.close()

    if not os.path.exists("baida.csv"):
        get_baida_list()
    with open('baida.csv', 'r') as f:
        reader = csv.reader(f)
        f_w = csv.writer(f)
        i = 1
        for row in reader:
            if i == 1:
                i = i + 1
                continue
            print(row)
            if row[1] == "no":
                try:
                    tempuid = int(row[0])
                    up_f = func_user(tempuid, True)
                    # [item['mid'], item['uname']]
                    for item in up_f:
                        try:
                            func_user(int(item[0]))
                        except Exception as e:
                            print(e)
                            print("——我失败了，定位1——")

                    print("\n" + str(row[0]) + " " + " 我也想知道他叫什么呀" + "我读完了")
                except Exception as e:
                    print(e)
                    print("——我失败了，定位2——")
        f.close()
    with open('data1fb.csv', 'r', encoding="utf-8",errors='ignore') as f:
        reader = csv.reader(f)
        f_csv = csv.writer(f)
        i = 1
        for row in reader:
            if i == 1:
                i = i + 1
                continue
            print(row)
            if row[1] not in umid:
                try:
                    func_user(int(row[1]))  # 这里加个try
                except Exception as e:
                    print(e)
                    print("——我失败了，定位3——")
            else:
                print("读过了")
    f.close()





def creat_csv():
    headers = ['user_uid', 'following_uid', 'nickname']
    with open('Infor_Recommendation/data1.csv', 'w', newline='', encoding='utf-8')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f.close()


def func_user(uid, getlist_only=False):
    '''
    用此函数爬取用户的关注列表
    :param uid: 用户uid
    :param getlist_only: 是否只需要爬取用户信息，而不用判断用户是否已在数据集中
    :return:
    '''
    up_info = []
    global umid
    if uid not in umid or getlist_only:
        try:
            follows = bilibili_api.user.get_followings(int(uid))  # 新的api不一样了
        except Exception as e:
            print("读取关注列表出错了" + e)
        # test_txt(follows)
        # print(type(follows))#list
        for item in follows:
            up_info.append([item['mid'], item['uname']])
            # {'mid': 648113003}
        if uid not in umid:
            fun_save(up_info, uid)
            umid.append(uid)
            with open('already_list.csv', 'a', newline='', encoding='utf-8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow([uid])
                f.close()

        print(str(len(up_info)))
        return up_info


def fun_save(list_followings, uid):
    # headers = ['user_uid', 'following_uid']
    rows = []
    for fw in list_followings:
        rows.append([uid, fw[0], fw[1]])
    # print(str(rows))
    with open('Infor_Recommendation/user_item.csv', 'a', newline='', encoding='utf-8')as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(headers)
        f_csv.writerows(rows)
        f.close()


def get_baida_list():
    '''
    爬取2020年度B站百大UP主信息
    :return:up_info
    '''
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    agisurl = "https://www.bilibili.com/activity/web/view/data/814?csrf=68af6c61bc4f65f034c6ee8e6403af85"
    head = {'user-agent': useragent}
    r = requests.get(agisurl, headers=head)
    decoded = json.loads(r.text)
    details = decoded['data']['list']
    up_info = []
    for dd in range(len(details)):
        up_info.append(details[dd]['data']['uid'])
    headers = ['user_uid', 'done']
    with open('baida.csv', 'w', newline='', encoding='utf-8')as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        row1 = []
        for item in up_info:
            row1.append([item, "no"])
        f_csv.writerows(row1)
        f.close()
    return up_info


def get_rookie_list():

    url_rookie = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie"
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    head = {'user-agent': useragent}
    r_rookie = requests.get(url_rookie, headers=head)
    rookie_info = r_rookie.json()
    # print(rookie_info)
    rr = rookie_info['data']['list']
    r_info = []
    for line in rr:
        r_info.append(line['owner']['mid'])
        # print([line['owner']['mid'], line['owner']['name'], line['title'], line['desc']])
    with open('baida.csv', 'a', newline='', encoding='utf-8')as f:
        f_csv = csv.writer(f)
        row1 = []
        for item in r_info:
            row1.append([item, "no"])
        f_csv.writerows(row1)
        f.close()


if __name__ == '__main__':
    main()

