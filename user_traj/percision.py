import pymysql
import pickle
import re
from collections import Counter

def cal_percision(rec_list,test_list):
    #取排名最高的5个好友，获取每个好友所有额推荐地点
    #test_list为测试集计算得到的兴趣点轨迹，此时不考虑轨迹，只考虑地点
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(rec_list)
def cal_recall(rec_list, test_list):
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(test_list)


def get_rec_list(sorted_list):
    db = pymysql.connect("localhost","root","123456","user_trajectory")
    cursor = db.cursor()
    hit_t = 0
    rec_t = 0
    unhit_num = 0
    total_num = 0
    for sort_poi in sorted_list:
        for k, v in sort_poi.items():
            ori_poi_sql = """ SELECT REC_POI FROM rec_list_300_30 where DEVICEID='%s' """ % k
            cursor.execute(ori_poi_sql)
            ori_poi = cursor.fetchall()
            rec_users = [[users[0] for users in v[:5] if users[1] != 0.0]]
            rec_poi_sql = 'SELECT REC_POI FROM rec_list_300_30 where DEVICEID in %s '
            cursor.execute(rec_poi_sql, rec_users)
            rec_pois = cursor.fetchall()
            rec_poi = []
            for r in rec_pois:
                l_temp = re.split(",|\|", r[0])
                # l_temp = r[0].split(',')
                rec_poi.extend(l_temp)
            hit_num, total_rec_num = cal_percision({}.fromkeys(rec_poi).keys(), list(ori_poi[0][0].split(',')))
            if hit_num == 0:
                unhit_num += 1
            hit_t += hit_num
            rec_t += total_rec_num
            total_num += 1
    print("推荐未命中兴趣点数量为： %d" % unhit_num)
    print("推荐总数量为： %d" % total_num)
    print("推荐兴趣点总数量为： %d" % rec_t)
    print("推荐命中兴趣点总数量为： %d" % hit_t)


def insert_rec_db(cal_list):
    db = pymysql.connect("localhost","root","123456","user_trajectory")
    cursor = db.cursor()
    insert_list = []
    sql = 'INSERT INTO rec_list (DEVICEID, REC_POI) VALUES(%s,%s)'
    len_size = 0
    for cal_poi in cal_list:
        rec_poi_list = [tradj.get('typecode') for tradj in cal_poi.get('tradj')]
        rec_poi_str = ','.join(rec_poi_list)
        if len(rec_poi_str) > len_size:
            len_size = len(rec_poi_str)
        data = (cal_poi.get('deviceId'), rec_poi_str)
        insert_list.append(data)
    print(len_size)
    cursor.executemany(sql, insert_list)
    db.commit()
    db.close()

def get_rec_list_score(sorted_list):
    db = pymysql.connect("localhost","root","123456","user_trajectory")
    cursor = db.cursor()
    hit_t = 0
    rec_t = 0
    unhit_num = 0
    total_num = 0
    for sort_poi in sorted_list:
        for k, v in sort_poi.items():
            ori_poi_sql = """ SELECT REC_POI FROM rec_list_300_30 where DEVICEID='%s' """ % k
            cursor.execute(ori_poi_sql)
            ori_poi = cursor.fetchall()
            rec_users = [[users[0] for users in v if users[1] != 0.0]]
            rec_poi_sql = 'SELECT REC_POI FROM rec_list_300_30 where DEVICEID in %s '
            cursor.execute(rec_poi_sql, rec_users)
            rec_pois = cursor.fetchall()
            rec_poi = []
            for r in rec_pois:
                l_temp = re.split(",|\|", r[0])
                rec_poi.extend(l_temp)
            hit_num, total_rec_num = cal_percision({}.fromkeys(rec_poi).keys(), list(ori_poi[0][0].split(',')))
            if hit_num == 0:
                unhit_num += 1
            hit_t += hit_num
            rec_t += total_rec_num
            total_num += 1

def insert_rec_db_score():
    db = pymysql.connect("localhost","root","123456","user_trajectory")
    cursor = db.cursor()
    sql = 'SELECT ID, REC_POI FROM rec_list_300_30'
    sql_update ='UPDATE rec_list_300_30 SET SCORE_DICT = %s,MOST_COUNT = %s WHERE ID = %s'
    cursor.execute(sql)
    ori_scores = cursor.fetchall()
    param_list = []
    for score in ori_scores:
        score_list = re.split(",|\|", score[1])
        score_dict = Counter(score_list)
        most_count = score_dict.most_common(1)[0][1]
        score_str = str(score_dict)
        insert_param = (score_str, most_count, score[0])
        param_list.append(insert_param)
    cursor.executemany(sql_update, param_list)
    db.commit()
    db.close()
