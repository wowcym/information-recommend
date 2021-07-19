def recall(true, pred):
    """
    计算召回度：有多少正确的样本被预测出来
    :param true: dict, {user:[item1, item2]
    :param pred: dict, recommend list for each user. e.g.{user:[(user2, similarity)]}
    :return:
    >>> true = {"u1":["item1", "item2"]}
    >>> pred = {"u1":[("u2", 0.6), ("u3", 0.1)]}
    """
    pred_true = 0
    all_true = 0

    for user, items in pred.items():
        for item in items:
            v, _ = item[0], item[1]
            if v in true[user]:
                pred_true += 1
        all_true += len(true[user])
    if all_true == 0:
        return 0
    return pred_true*1.0 / all_true

def precision(true, pred):
    """
    计算准确度：有多少预测的结果是正确的
    :param true: dict, {user:[item1, item2]
    :param pred: dict, recommend list for each user. e.g.{user:[(user2, similarity)]}
    >>> true = {"u1":["item1", "item2"]}
    >>> pred = {"u1":[("u2", 0.6), ("u3", 0.1)]}
    :return:
    """
    pred_true = 0
    all_pred = 0
    for user,items in pred.items():
        for item in items:
            v, _ = item[0], item[1]
            if v in true[user]:
                pred_true += 1
            all_pred += 1
    if all_pred == 0:
        return 0
    return pred_true*1.0 / all_pred

def coverage(actual_items, recommend_items):
    """
    覆盖率，coverage = len(set(pred))/len(set(actual_items))
    :param actual_items: set(), all items.
    :param recommend_items: set(), all recommend items
    :return:
    >>> actual_items = set("item1", "item2")
    >>> recommend_items = set("item1")
    """
    if len(set(actual_items)) == 0:
        return 1
    return (len(set(recommend_items))*1.0)/len(set(actual_items))

def popularity(user_cf, train, test, N, K):
    """
    流行度，popularity means how many people have watched it. Log transformation is applied for stability.
    :param user_cf: recommend system.
    :param train: dict, the train set.
    :param test: dict, the test set.
    :param N: select top N items to recommend.
    :param K: select the moset K similar users.
    :return:
    >>> train = {"user":["item1", "item2"]}
    >>> test = {"user2":["item2"]}
    """
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            item_popularity[item] = item_popularity.get(item,0)+1
    ret = 0
    n = 0
    for user in test.keys():
        recommend_list = user_cf.recommend(user, N, K)
        for item,sim in recommend_list:
            ret += math.log(1 + item_popularity[item])
            n += 1
    if n == 0:
        return 0
    ret = ret*1.0/n
    return ret