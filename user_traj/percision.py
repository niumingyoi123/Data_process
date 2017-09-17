import pymysql
import pickle

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
                l_temp = r[0].split(',')
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

