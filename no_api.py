# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from wordcloud import WordCloud
import jieba.analyse

keywl = []
umid = 0


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def func_follow(startid=0):
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    # B站限制最多只能爬200的
    url = 'https://api.bilibili.com/x/relation/followings?vmid=' + str(startid) + '&pn=1&ps=200&order=desc&order_type' \
        # head = {'user-agent': useragent,'cookie':cookie}
    head = {'user-agent': useragent}
    result = requests.get(url, headers=head)
    r = result.json()
    print(result.text)
    '''
    file = open(text1.txt', mode='w')
    file.write(str(r))
    file.close()
    '''
    users = r['data']['list']
    user_info = []
    for user in users:
        use_sign = remove_keywords(user['sign'])
        if 'official_verify' in user:
            user_info.append([user['mid'], user['uname'], use_sign, user['official_verify']['desc']])
        else:
            user_info.append([user['mid'], user['uname'], use_sign, []])
    # 保存up主信息
    if user_info:
        filename = 'user_follows_' + str(startid) + '.txt'
        file = open(filename, 'w')
        # file.write(str(user_info))
        for i in range(len(user_info)):
            line = str(user_info[i]) + '\n'
            file.write(line)
        file.close()
    # data=result.


# 去除部分无效关键字
def remove_keywords(sign):
    global keywl
    keywords_textrank = jieba.analyse.textrank(sign)
    # print(type(keywords_textrank))
    block_words = ['合作', '工作室', '私信', '联系', '工作', '商务', '微信', '账号', '邮箱', '公众', '关注']
    for kw in block_words:
        if kw in keywords_textrank:
            keywords_textrank.remove(kw)
    # print(keywords_textrank)
    keywl.extend(keywords_textrank)
    return keywords_textrank


def wordcloud(key_word):
    global umid
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
    ww.to_file('词云_' + umid + '.png')
    return


def func_user_info(mid):
    url_user = 'https://api.bilibili.com/x/space/acc/info?mid=' + str(mid)
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 ' \
                'Safari/537.36 '
    head = {'user-agent': useragent}
    user_info = requests.get(url_user, headers=head)
    f = user_info.json()
    # print(f)
    user_name = f['data']['name']
    user_sex = f['data']['sex']
    user_face = f['data']['face']  # 后续做前端可能会用到
    user_sign = f['data']['sign']
    user_level = f['data']['level']
    print(user_name, "性别：" + user_sex, str(user_level) + '级号', "简介：" + user_sign, sep='\n')
    info = {"name": user_name, "性别": user_sex, "等级": user_level, "简介": user_sign}
    return info


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('up——up')
    while 1:
        umid = input('请输入你的B站UID号:')
        if umid.isdigit():
            func_follow(int(umid))  # 爬取用户的关注
            func_user_info(int(umid))
            # print(keywl)
            wordcloud(keywl)
            break
        else:
            print('您输入的UID号不正确，请确认后再输入')

    # func(12881338)
    # 13101988#AK

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
