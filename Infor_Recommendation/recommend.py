import math
from math import exp
import pandas as pd
import numpy as np
import pickle
import time

class ItemCF(object):
    """
    物品协同过滤，根据用户浏览过的物品推荐相似物品
    整个过程包含两个步骤：
    （1）计算物品之间的相似度；
    （2）根据物品的相似度和用户的历史行为给用户生成推荐列表；
    """
    
    def train(self, user_items, alpha=0.5, normalization=False):
        """
        训练模型
        :return:
        """
        self.user_items = user_items
        # 计算物品的协同矩阵
        # 基于哈利波特问题改进的ItemCF 
        self.item_sim_matrix = self.improved_item_similarity2(user_items, alpha=alpha, normalization=normalization)

        return self.item_sim_matrix

    
    def improved_item_similarity2(self, user_items, alpha=0.5, normalization=False):
        """
        :param user_items: {user1:[movie1,movie2], user2:[movie1]}
        :return: W: {items1: {item2: sim12, item3:sim13}}
        """
        # 计算物品间存在的共同用户数
        C = dict()
        # 物品总数
        N = dict()
        # 统计物品间的相似权重（通过出现过多少次来判断）
        for user, items in user_items.items():
            """
            items为该user所喜爱的物品集合
            对该集合进行一个遍历
            """
            for i in items:
                # 初始化N，并统计i出现的数目
                N[i] = N.get(i,0) + 1
                if i not in C:
                    C[i] = dict()
                for j in items:
                    if i == j:
                        continue
                    # 1/math.log(1+len(items)为对该user的惩罚，其喜欢的物品越多，贡献度越低
                    C[i][j] = C[i].get(j,0) + 1/math.log(1+len(items))

        # 计算最终的相似矩阵W
        W = dict()
        for i, related_items in C.items():
            if i not in W:
                W[i] = dict()
            for j, cij in related_items.items():
                W[i][j] = cij / (N[i]**(1-alpha) * N[j]**alpha)
                
        # 归一化处理
        if normalization:
            for i, item_list in W.items():
                item_list = [item/max(item_list) for item in item_list]
                W[i] = item_list
        return W

    def recommend(self, user, N, K):
        """
        根据用户历史数据进行推荐
        :param user:
        :param N: 被推荐物品的数量
        :param K: 最相似用户的数量
        :return:  推荐物品的字典，格式为, {item: similarity}
        """
        already_items = set(self.user_items.get(user, set()))
        recommend_items = dict()

        for i in already_items:
            # sorted为基于第二列的负数进行升序排列（也就是降序排列）
            for j, sim in sorted(self.item_sim_matrix.get(i,dict()).items(), key=lambda x:-x[1])[:K]:
                if j in already_items:
                    continue
                # 将相似性相加汇总
                recommend_items[j] = recommend_items.get(j,0) + sim
        # 将推荐的物品进行降序排列
        recommend_item_list = sorted(recommend_items.items(), key=lambda x:-x[1])[:N]
        return recommend_item_list

    def recommend_users(self, users, N, K):
        """

        :param users:
        :param N: 被推荐物品的数量
        :param K: 最相似用户的数量
        :return: 字典，格式为， {user:[movie1, movie2]}
        """
        recommend_result = dict()
        for user in users:
            recommend_item_list = self.recommend(user, N, K)
            recommend_result[user] = recommend_item_list
        return recommend_result
     
class UserCF(object):
    """
    用户协同过滤，根据相似用户推荐内容
    整个过程包含两个步骤：
    （1）找到和目标用户兴趣相似的用户集合；
    （2）根据该集合中用户喜欢的，且目标用户之前没见过的物品推荐给目标用户
    """
    def train(self, user_items):
        """
        训练模型
        :return:
        """
        self.user_items = user_items
        # 计算用户的协同矩阵
        self.user_sim_matrix = self.user_similarity(user_items)
        return self.user_sim_matrix


    def user_similarity(self, user_items):
        """
        生成item_users的倒排表
        主要是因为很多用户并没有对同样的物品产生过行为，数据是稀疏的
        :param user_items: {user1:[movie1,movie2], user2:[movie1]}
        :return:
        """
        item_users = dict()
        for u, items in user_items.items():
            for i in items:
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)

        # 计算用户间具有都出现过的物品
        C = dict()
        N = dict()
        for item, users in item_users.items():
            """
            users为喜欢过该item的用户合集
            对该集合进行一个遍历
            """
            for u in users:
                N[u] = N.get(u,0) + 1
                if u not in C:
                    C[u] = dict()
                for v in users:
                    if v == u:
                        continue
                    C[u][v] = C[u].get(v,0) + 1

        # 计算最终的相似度矩阵W
        W = dict()
        for u, related_users in C.items():
            if u not in W:
                W[u] = dict()
            for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt(N[u] * N[v])

        return W

    def recommend(self, user, N, K):
        """
        根据用户推荐物品
        :param user:
        :param N: 被推荐物品的数量
        :param K: 最相似用户的数量
        :return: 被推荐物品及相似度的字典，其存储格式为, {item: similarity}
        """
        already_items = set(self.user_items.get(user, set()))
        recommend_items = dict()
        for v, sim in sorted(self.user_sim_matrix.get(user,dict()).items(), key=lambda x:-x[1])[:K]:
            for item in self.user_items[v]:
                if item in already_items:
                    continue
                recommend_items[item] = recommend_items.get(item,0) + sim
        recommend_item_list = sorted(recommend_items.items(), key=lambda x:-x[1])[:N]
        return recommend_item_list

    def recommend_users(self, users, N, K):
        """
        运行整个模型，可以用于存储模型，加快运行速率
        :param users:
        :param N: 被推荐物品的数量
        :param K: 最相似用户的数量
        :return: 字典，其存储格式为, {user:[movie1, movie2]}
        """
        recommend_result = dict()
        for user in users:
            recommend_item_list = self.recommend(user, N, K)
            recommend_result[user] = recommend_item_list
        return recommend_result
    
class HiddenSemantics(object):
    '''
    隐语义
    '''
    def getUserNegativeItem(self, frame, userID):
        '''
        获取用户负反馈物品：热门但是用户没有进行过评分与正反馈数量相等
        :param frame: ratings数据
        :param userID:用户ID
        :return: 负反馈物品
        '''
        userItemlist = list(set(frame[frame['user_uid'] == userID]['following_uid']))                       #用户评分过的物品
        otherItemList = [item for item in set(frame['following_uid'].values) if item not in userItemlist] #用户没有评分的物品
        itemCount = [len(frame[frame['following_uid'] == item]['user_uid']) for item in otherItemList]      #物品热门程度
        series = pd.Series(itemCount, index=otherItemList)
        series = series.sort_values(ascending=False)[:len(userItemlist)]                            #获取正反馈物品数量的负反馈物品
        negativeItemList = list(series.index)
        return negativeItemList
    
    def getUserPositiveItem(self, frame, userID):
        '''
        获取用户正反馈物品：用户评分过的物品
        :param frame: ratings数据
        :param userID: 用户ID
        :return: 正反馈物品
        '''
        series = frame[frame['user_uid'] == userID]['following_uid']
        positiveItemList = list(series.values)
        return positiveItemList
    
    def initUserItem(self, frame, userID=1):
        '''
        初始化用户正负反馈物品,正反馈标签为1,负反馈为0
        :param frame: ratings数据
        :param userID: 用户ID
        :return: 正负反馈物品字典
        '''
        positiveItem = self.getUserPositiveItem(frame, userID)
        negativeItem = self.getUserNegativeItem(frame, userID)
        itemDict = {}
        for item in positiveItem: itemDict[item] = 1
        for item in negativeItem: itemDict[item] = 0
        return itemDict
    
    def initUserItemPool(self, frame, userID):
        '''
        初始化目标用户样本
        :param userID:目标用户
        :return:
        '''
        userItem = []
        for id in userID:
            itemDict = self.initUserItem(frame, userID=id)
            userItem.append({id:itemDict})
        return userItem
 
    def initPara(self, userID, itemID, classCount):
        '''
        初始化参数q,p矩阵, 随机
        :param userCount:用户ID
        :param itemCount:物品ID
        :param classCount: 隐类数量
        :return: 参数p,q
        '''
        arrayp = np.random.rand(len(userID), classCount) #构造p矩阵，[0,1]内随机值
        arrayq = np.random.rand(classCount, len(itemID)) #构造q矩阵，[0,1]内随机值
        p = pd.DataFrame(arrayp, columns=range(0,classCount), index=userID)
        q = pd.DataFrame(arrayq, columns=itemID, index=range(0,classCount))
    
        return p,q
 
    def initModel(self, frame, classCount):
        '''
        初始化模型：参数p,q,样本数据
        :param frame: 源数据
        :param classCount: 隐类数量
        :return:
        '''
        userID = list(set(frame['user_uid'].values))
        itemID = list(set(frame['following_uid'].values))
        p, q = self.initPara(userID, itemID, classCount)    #初始化p、q矩阵
        userItem = self.initUserItemPool(frame,userID)      #建立用户-物品对应关系
        return p, q, userItem
 
    def latenFactorModel(self, frame, classCount, iterCount, alpha, lamda):
        '''
        隐语义模型计算参数p,q
        :param frame: 源数据
        :param classCount: 隐类数量
        :param iterCount: 迭代次数
        :param alpha: 步长
        :param lamda: 正则化参数
        :return: 参数p,q
        '''
        p, q, userItem = self.initModel(frame, classCount)
        for step in range(0, iterCount):
            for user in userItem:
                for userID, samples in user.items():
                    for itemID, rui in samples.items():
                        eui = rui - self.lfmPredict(p, q, userID, itemID)
                        for f in range(0, classCount):
                            print('step %d user %d class %d' % (step, userID, f))
                            p[f][userID] += alpha * (eui * q[itemID][f] - lamda * p[f][userID])
                            q[itemID][f] += alpha * (eui * p[f][userID] - lamda * q[itemID][f])
            alpha *= 0.9
        return p, q
 
    def sigmod(self, x):
        '''
        单位阶跃函数,将兴趣度限定在[0,1]范围内
        :param x: 兴趣度
        :return: 兴趣度
        '''
        y = 1.0/(1+exp(-x))
        return y

    def lfmPredict(self, p, q, userID, itemID):
        '''
        利用参数p,q预测目标用户对目标物品的兴趣度
        :param p: 用户兴趣和隐类的关系
        :param q: 隐类和物品的关系
        :param userID: 目标用户
        :param itemID: 目标物品
        :return: 预测兴趣度
        '''
        # 注意这里用loc，iloc是按照序号索引，会报错
        p = np.mat(p.loc[userID].values)
        q = np.mat(q[itemID].values).T
        r = (p * q).sum()
        r = self.sigmod(r)
        return r
 
    def Recommend(self, frame, userID, p, q, N):
        '''
        推荐TopN个物品给目标用户
        :param frame: 源数据
        :param userID: 目标用户
        :param p: 用户兴趣和隐类的关系
        :param q: 隐类和物品的关系
        :param TopN: 推荐数量
        :return: 推荐物品
        '''
        userItemlist = list(set(frame[frame['user_uid'] == userID]['following_uid']))
        otherItemList = [item for item in set(frame['following_uid'].values) if item not in userItemlist]
        predictList = [self.lfmPredict(p, q, userID, itemID) for itemID in otherItemList]
        series = pd.Series(predictList, index = otherItemList)
        series = series.sort_values(ascending = False)[:N]
        return series
    
class TagsRecommend(object):
    '''
    基于标签的算法推荐算法，基本思路：
    统计每个用户最常用的标签，然后找到具有这些标签的最热门物品推荐给这个用户
    基本参数：
    标签数据records[i] = [user, item, tag];
    用户u打过标签b的次数user_tags[u][b] = nu,b
    物品i被打过标签b的次数tag_items[b][i] = nb,i
    '''
    def addValueToMat(self, theMat,key,value):  
        '''
        用于进行矩阵初始化
        :param 
        :param
        :param
        '''
        #如果key没出先在theMat中  
        if key not in theMat:
            theMat[key] = dict();  
            theMat[key][value] = 1;  
        else:  
            if value not in theMat[key]:  
                theMat[key][value] = 1;  
            else:  
                theMat[key][value] += 1;#若有值，则递增
   
    def InitStat(self, records):
        '''
        初始化用户打标签矩阵user_tags、物品被打标签矩阵tag_items与用户物品间关系user_items
        :param records: 用户标签数据记录
        :return: 负反馈物品
        '''
        user_tags = dict()
        tag_items = dict()
        user_items = dict()
        for row, row_index in records.iterrows():
            user = row_index[0]
            item = row_index[1]
            tag = row_index[2]
            self.addValueToMat(user_tags, user, tag)
            self.addValueToMat(tag_items, tag, item)
            self.addValueToMat(user_items, user, item)
        return user_tags, tag_items, user_items

    def Recommend(self, user_uid, N):
        '''
        :param  user_uid: 用户的uid
        :return recommend_item: 推荐关注列表
        '''
        recommend_items = dict()
        tagged_items = self.user_items[user_uid]
        for tag, wut in self.user_tags[user_uid].items():
            for item, wti in self.tag_items[tag].items():
                # 如果物品已经被打过标签，则不推荐他们
                if item in tagged_items:
                    continue
                if item not in recommend_items:
                    recommend_items[item] = wut * wti
                else:
                    recommend_items[item] += wut * wti
        recommend_item_list = sorted(recommend_items.items(), key=lambda x:-x[1])[:N]
        return recommend_item_list




    
    
    