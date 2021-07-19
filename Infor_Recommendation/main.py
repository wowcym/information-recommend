import sys
import numpy as np
import pandas as pd

sys.path.append('../')
from Infor_Recommendation import train
from Infor_Recommendation.recommend import UserCF
from Infor_Recommendation.recommend import ItemCF
from Infor_Recommendation.recommend import HiddenSemantics
from Infor_Recommendation.recommend import TagsRecommend

# 这里输入需要查询的uid
file_name = "G:\信息推荐系统课程设计\data1.csv"
all_data_df = pd.read_csv(file_name)
#user_uid = 82389
user_uid = 18358250
#user_uid = 11073

'''
file_name = "/Users/air/Desktop/信息推荐系统课程设计/tag_data.csv"

# file_name = "/Users/air/Desktop/信息推荐系统课程设计/data1_13w.csv"
# 下面这个需要读取tags的文件
#file_name = "/Users/air/Desktop/ml-latest-small/tags.csv"

# 导入数据
all_data_df = pd.read_csv(file_name, encoding = "utf-8") 
# all_data_df.drop('timestamp', 1, inplace=True)
'''
'''
###### 生成并存储模型 #######
# 物品协同、用户协同
user_cf, user_item_dict = train.train_user_cf(all_data_df)
item_cf, user_item_dict = train.train_item_cf(all_data_df)
np.save('user_item_dict', user_item_dict) 
W0 = user_cf.train(user_item_dict)
np.save('userCF_W.npy', W0) 
W1 = item_cf.train(user_item_dict)
np.save('itemCF_W.npy', W1)

# 标签推荐
tags_recommend = TagsRecommend()
user_tags, tag_items, user_items = tags_recommend.InitStat(all_data_df)
np.save('user_tags.npy', user_tags)
np.save('tag_items.npy', tag_items)
np.save('user_items.npy', user_items)

# 隐语义
all_data_df['rating'] = 5
a = HiddenSemantics()
p, q = a.latenFactorModel(all_data_df, 5, 3, 0.02, 0.01 )
q.to_json('q.json')
p.to_json('p.json')
'''


N = 5
K = 20

def recommend_IC(uid):
    item_cf = ItemCF()
    item_cf.item_sim_matrix = np.load('itemCF_W.npy', allow_pickle=True).item()
    item_cf.user_items = np.load('user_item_dict.npy', allow_pickle=True).item()
    recommend = item_cf.recommend(user_uid, N = N, K = K)
    return recommend
    
def recommend_UC(uid):
    user_cf = UserCF()
    user_cf.user_sim_matrix = np.load('userCF_W.npy', allow_pickle=True).item()
    user_cf.user_items = np.load('user_item_dict.npy', allow_pickle=True).item()
    recommend = user_cf.recommend(user_uid, N = N, K = K)
    return recommend

def recommend_Tags(uid):
    tags_recommend = TagsRecommend()
    tags_recommend.user_tags = np.load('user_tags.npy', allow_pickle=True).item()
    tags_recommend.tag_items = np.load('tag_items.npy', allow_pickle=True).item()
    tags_recommend.user_items = np.load('user_items.npy', allow_pickle=True).item()
    recommend = tags_recommend.Recommend(uid, N = N)
    return recommend

def recommend_Hidden(uid):
    H_S = HiddenSemantics()
    p = pd.read_json('p.json')
    q = pd.read_json('q.json')
    recommend = H_S.Recommend(all_data_df, uid, p, q, N)
    return recommend
    

# print(recommend_IC(user_uid))
# print(recommend_UC(user_uid))
# print(recommend_Tags(user_uid))

'''
# 参数分别为源数据、目标用户id、用户兴趣和隐类的关系矩阵p、隐类和物品的关系矩阵q
b = a.recommend(all_data_df, user_uid, p, q)
'''

# print(recommend_Hidden(user_uid))


