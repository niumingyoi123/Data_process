import pymysql
import json
import pickle

def insert_db():
    db = pymysql.connect("localhost", "root", "Meituan-0502", "user_trajectory")
    cursor = db.cursor()
    geo_file = open("/Users/niumingyi/Downloads/data/beijing2_geo_data", "r")
    geo_datas = geo_file.readlines()
    geo_file.close()
    list = []
    for geo_data in geo_datas:
        geo_data_json = json.loads(geo_data)
        data = (
        geo_data_json['timestamp'], geo_data_json['deviceid'], geo_data_json['longitude'], geo_data_json['latitude'])
        list.append(data)
        sql = 'INSERT INTO beijing (TIMESTAMP,DEVICEID,LONGITUDE,LATITUDE) VALUES(%s,%s,%s,%s)'
    # try:
    cursor.executemany(sql, list)
    db.commit()
    # except:
    #     db.rollback()
    db.close()

def insert_rec_db(cal_list):
    db = pymysql.connect("localhost", "root", "Meituan-0502", "user_trajectory")
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