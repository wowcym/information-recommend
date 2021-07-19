import sys
import math
import numpy as np
import pandas as pd

sys.path.append('../')
from recommend import UserCF
from recommend import ItemCF
from recommend import HiddenSemantics
import evaluate


def train_user_cf(train_df):
    user_cf = UserCF()
    # 将train_df按照user_uid做分组，并将分组结果中的following_uid以list的形式进行存储
    user_item_df = train_df.groupby("user_uid")["following_uid"].apply(list).reset_index(name="FollowingIDList")
    # 将两个列表合成为一个字典，keys为user_uid，values为followingIDList
    user_item_dict = dict(zip(user_item_df["user_uid"], user_item_df["FollowingIDList"]))
    return user_cf, user_item_dict

def train_item_cf(train_df):
    item_cf = ItemCF()
    user_item_df = train_df.groupby("user_uid")["following_uid"].apply(list).reset_index(name="FollowingIDList")
    user_item_dict = dict(zip(user_item_df["user_uid"], user_item_df["FollowingIDList"])) 
    return item_cf, user_item_dict


def evaluate(user_cf, train_dict, test_dict, N, K):
    """
    模型评估
    :param N: 被推荐物品的数量
    :param K: 最相似用户的数量
    :return:
    """
    recommend_dict = user_cf.recommend_users(test_dict.keys(), N = N, K = K)

    # 召回率、精确率
    recall_val = evaluate.recall(true = test_dict, pred = recommend_dict)
    precision_val = evaluate.precision(true = test_dict, pred = recommend_dict)

    actual_items = set()
    for item_list in train_dict.values():
        for item in item_list:
            if item not in actual_items:
                actual_items.add(item)
    print("actual_items", len(actual_items))

    recommend_items = set()
    for item_list in recommend_dict.values():
        for (item,sim) in item_list:
            if item not in recommend_items:
                recommend_items.add(item)
    print("recommend_items", len(recommend_items))
    
    # 覆盖度和流行度
    coverage_val = evaluate.coverage(actual_items = actual_items, recommend_items = recommend_items)
    popularity_val = evaluate.popularity(user_cf = user_cf, train = train_dict, test = test_dict, N = N, K = K)

    return [recall_val,precision_val,coverage_val,popularity_val]


# 输入输出参数同上面保持一致
def evaluate_user_cf(user_cf, train_dict, test_dict, N, K):
    a = evaluate(user_cf, train_dict, test_dict, N, K)
    print('用户协同过滤模型的参数情况为：召回率' + str(a[0]) + '准确率' + str(a[1]) + '覆盖率' + str(a[2]) + '流行度' + str(a[3]))
    
def evaluate_item_cf(user_cf, train_dict, test_dict, N, K):
    a = evaluate(user_cf, train_dict, test_dict, N, K)
    print('物品协同过滤模型的参数情况为：召回率' + str(a[0]) + '准确率' + str(a[1]) + '覆盖率' + str(a[2]) + '流行度' + str(a[3]))


