import os
import requests
import json
import jieba.analyse
import bilibili_api

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
            'Safari/537.36 '

def func_upinfo():
    agisurl = "https://www.bilibili.com/activity/web/view/data/814?csrf=68af6c61bc4f65f034c6ee8e6403af85"
    url_rookie = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=rookie"
    # print(useragent)
    head = {'user-agent': useragent}
    r = requests.get(agisurl)
    decoded = json.loads(r.text)
    details = decoded['data']['list']
    print(details)
    up_info = []
    # print('index', 'name', 'uid', 'description', sep='\t')
    for dd in range(len(details)):
        # download images
        # print(details[dd]['name'])
        # print(details[dd]['data']['face'])
        # download('http:' + details[dd]['data']['face'], str(dd).rjust(3,'0') + '-' + details[dd]['name'])
        description = str(jieba.analyse.textrank(details[dd]['data']['desc'])).replace(',', ' ')
        up_info.append([details[dd]['data']['uid'], details[dd]['name'], description])
    r_rookie = requests.get(url_rookie, headers=head)
    rookie_info = r_rookie.json()
    # print(rookie_info)
    rr = rookie_info['data']['list']
    r_info = []
    for line in rr:
        description_rookie = str(jieba.analyse.textrank(line['desc'])).replace(',', ' ')
        r_info.append([line['owner']['mid'], line['owner']['name'], line['tname'], line['title'], description_rookie])
        # print([line['owner']['mid'], line['owner']['name'], line['title'], line['desc']])
    fun_save('up_info_file/top100_up.txt', up_info)
    fun_save('up_info_file/rookie_up.txt', r_info)


def fun_save(file_name, list1):
    file = open(file_name, mode='w', encoding='utf-8')
    for i in range(len(list1)):
        line = str(list1[i]).replace(',', '\n').replace('[', '').replace(']', '') + '\n\n'
        file.write(line)
    file.close()


def func_video_info(bvid):
    '''
    url_video = "https://api.bilibili.com/x/space/arc/search?mid=" + str(mid) + "&pn=1&ps=25&index=1&jsonp=jsonp"
    head = {'user-agent': useragent}
    result = requests.get(url_video, headers=head)
    r = result.json()
    print(r)
    '''
    video_info = bilibili_api.video.get_video_info(bvid)
    tags=bilibili_api.video.get_tags(bvid)#list
    #print(tags)
    tag=[]
    for item in tags:
        tag.append(item['tag_name'])
    print(tag)




#拿来保存测试信息的，别管
def test_txt(things):
    file = open('test_info.txt', 'w')
    file.write(str(things))
    file.close()

if __name__ == '__main__':
    print('我要开始爬取up信息啦')
    func_upinfo()
    test_bvid = 'BV1Si4y1s7Sj'
    func_video_info(test_bvid)
