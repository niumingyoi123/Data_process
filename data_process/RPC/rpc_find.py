from util.GaoDe_api import districts_filter
from geojson import Point
from geojson_utils import point_in_polygon
import json,pymysql
from datetime import timedelta

def resiednt_filter(district,d):
    polygon = districts_filter(district)
    geo_file = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\geo_data_%d' % d, "r")
    geo_datas = geo_file.readlines()
    file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\%s_geo_data'%district, 'a')
    for geo_data in geo_datas:
        geo_data_json = json.loads(geo_data)
        point = Point((float(geo_data_json['longitude']),float(geo_data_json['latitude'])))
        if point_in_polygon(point,polygon):
            file_object.write(json.dumps(geo_data_json) + '\n')


def get_traj_rpc(times_threshold,time_span):
    db = pymysql.connect("localhost", "root", "", "user_trajectory")

    cursor = db.cursor()

    sql = """ SELECT * FROM dongcheng WHERE DEVICEID in (SELECT DEVICEID FROM dongcheng GROUP BY DEVICEID HAVING COUNT(DEVICEID)>%d) ORDER BY DEVICEID,`TIMESTAMP`
    """%times_threshold
    rpc = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        deviceid = result[0][2]
        start_time = result[0][1]
        end_time = result[0][1]
        for row in result:
            if row[2]!=deviceid:
                if end_time-start_time>time_span:
                    rpc.append(deviceid)
                deviceid = row[2]
                start_time = row[1]
                end_time = row[1]
            else:
                end_time = row[1]
        return rpc
    except:
        print("Error")

# rpc = get_traj_rpc(10,timedelta(days=5))
# print(rpc)


