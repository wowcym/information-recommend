# 本函数通过用户的uid 爬取其关注列表
# 根据其关注列表，爬取相关up的信息和视频bvid
# 通过bvid获取相关tag信息,并生成词云
import bilibili_api
import time
from wordcloud import WordCloud
import proxypool


# import MySQLdb
up_info = []
bvid_list = []
tag_sum = []


def main(umid):
    func_user(umid)
    # func_video_info('375375')# 会有网络异常
    i = 0
    # 差不多每50个会失败一段时间
    # 我觉得要那么多up意义也不大，而且太慢了
    # 所以我只爬取前20个up的信息（前20是最新关注的前20）
    for item in up_info:
        try:
            func_video_info(item[0]['mid'])
            # time.sleep(3) 毫无意义
            # print(i)
            i = i + 1
            if (i == 19):
                break
        except Exception as e:
            print("读取" + str(item[0]['mid']) + "视频信息失败")
            # time.sleep(300)
            print(e)

        # else:
        # print("读取成功")
    # print(bvid_list)
    fun_save('user_info/follow_bvid.txt', bvid_list)
    func_video_tag()


def func_video_tag():
    global tag_sum
    sum = 0
    print("——————在爬取tag————————")

    # 暂时将所有的tag都放到一起
    for item in bvid_list:
        for k in item.values():
            count1 = 0
            for bid in k:
                # print(bid)
                count1 = count1 + 1
                try:
                    tag_l = bilibili_api.video.get_tags(bid)
                    count = 0
                    for l in tag_l:
                        tag_sum.append(l['tag_name'])
                        count = count + 1
                        print(l['tag_name'])
                        if count == 2:
                            break
                except:
                    print('我死了')
                    break
                if count1 == 20:
                    break

    wordcloud(tag_sum)
    print(tag_sum)
    fun_save('user_info/all_tag.txt', tag_sum)


# 得到用户关注人基本信息：mid+用户名+用户官方title
def func_user(uid):
    global up_info
    follows = bilibili_api.user.get_followings(int(uid))
    # test_txt(follows)
    # print(type(follows))#list
    for item in follows:
        up_info.append([{'mid': item['mid']}, {'uname': item['uname']}, {'desc': item['official_verify']['desc']}])
        # [{'mid': 648113003}, {'uname': '沈逸老师'}, {'desc': '复旦大学教授，《逸语道破》主讲人、bilibili 2020百大UP主'}]
    print(str(up_info))
    fun_save('user_info/up_info.txt', up_info)
    print(str(len(up_info)))
    return


def func_video_info(uid):
    # print('在读取' + str(uid) + '的视频信息')
    r_video = bilibili_api.user.get_videos(int(uid))
    # print(r_video)
    # print(type(r_video))
    # test_txt(r_video)
    list1 = []
    count=0
    for item in r_video:
        list1.append(item['bvid'])
        count=count+1
        if(count==20):
            break
    bvid_list.append({uid: list1})
    print(str(uid) + '共发布了' + str(len(list1)) + '条视频')


def fun_save(file_name, list1):
    file = open(file_name, mode='w', encoding='utf-8')
    for i in range(len(list1)):
        line = str(list1[i]).replace(',', '\n').replace('[', '').replace(']', '') + '\n\n'
        file.write(line)
    file.close()


# 拿来保存测试信息的，别管
def test_txt(things):
    file = open('test_info.txt', mode='w', encoding='utf-8')
    file.write(str(things))
    file.close()


def wordcloud(key_word):
    '''
    AK = open('try_AK.txt', encoding='utf-8').read()
    tyr_wd = jieba.cut(AK,cut_all=True)
    words = " ".join(tyr_wd)
    print(words)
    '''
    words = " ".join(key_word)
    w = WordCloud(width=1000, height=700, background_color='white', font_path='/fonts/FZYTK.TTF')
    ww = w.generate(words)
    # print('我运行了')
    ww.to_file('词云_.png')
    return


if __name__ == '__main__':
    print('我要开始工作了')
    while 1:
        umid = input('请输入你的B站UID号:')
        # umid = '13101988'
        if umid.isdigit():
            main(umid)
            break
        else:
            print('您输入的UID号不正确，请确认后再输入')
