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
    for sort_poi in sorted_list:
        for k, v in sort_poi.items():
            ori_poi_sql = """ SELECT REC_POI FROM rec_list where DEVICEID='%s' """ % k
            cursor.execute(ori_poi_sql)
            ori_poi = cursor.fetchall()
            rec_users = [[users[0] for users in v[:5] if users[1] != 0.0]]
            print(rec_users)
            rec_poi_sql = 'SELECT REC_POI FROM rec_list where DEVICEID in %s '
            cursor.execute(rec_poi_sql, rec_users)
            rec_pois = cursor.fetchall()
            rec_poi = []
            for r in rec_pois:
                l_temp = r[0].split(',')
                rec_poi.extend(l_temp)
            print(cal_percision(rec_poi, ori_poi))


# f_cal = open('cal_list', 'rb')
# cal_list = pickle.load(f_cal)
# f_cal.close()
# insert_rec_db(cal_list)
f_sorted = open('sorted_list', 'rb')
sorted_list = pickle.load(f_sorted)
f_sorted.close()
# print(cal_list)
# print(sorted_list)

get_rec_list(sorted_list)
