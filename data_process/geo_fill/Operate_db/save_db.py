import pymysql
import json

db = pymysql.connect("localhost","root","","user_trajectory")
cursor = db.cursor()
geo_file = open("F:/new_geo_data","r")
geo_datas = geo_file.readlines()
geo_file.close()
list=[]
for geo_data in geo_datas:
    geo_data_json = json.loads(geo_data)
    data = (geo_data_json['timestamp'],geo_data_json['deviceid'],geo_data_json['longitude'],geo_data_json['latitude'])
    list.append(data)
sql = """INSERT INTO USER_TRAJ(TIMESTAMP,DEVICEID,LONGITUDE,LATITUDE) VALUES(%s,%s,%s,%s)"""
try:
    cursor.executemany(sql, list)
    db.commit()
except:
    db.rollback()
db.close()

