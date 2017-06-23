def cal_percision(rec_list,test_list):
    #取排名最高的10个好友，每个好友推荐最多5个地点，rec_list长度为50
    #test_list为测试集计算得到的兴趣点轨迹，此时不考虑轨迹，只考虑地点
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(rec_list)
def cal_recall(rec_list, test_list):
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(test_list)



