from util.GaoDe_api import districts_filter
from geojson import Point
from geojson_utils import point_in_polygon
import json,pymysql
from datetime import timedelta

def resiednt_filter(district):
    polygon = districts_filter(district)
    geo_file = open('/Users/niumingyi/Downloads/data/new_geo_data', "r")
    geo_datas = geo_file.readlines()
    file_object = open('/Users/niumingyi/Downloads/data/beijing2_geo_data', 'a')
    r_l = []
    i = 0
    for geo_data in geo_datas:
        i += 1
        geo_data_json = json.loads(geo_data)
        point = Point((float(geo_data_json['longitude']),float(geo_data_json['latitude'])))
        if point_in_polygon(point,polygon):
            r_l.append(json.dumps(geo_data_json))
            print("in district mark %d" % i)
            # file_object.write(json.dumps(geo_data_json) + '\n')
        else:
            print("out of district mark %d" % i)
    file_object.write('\n'.join(r_l))

# resiednt_filter("北京")


def fetch_rpc(times_threshold, time_span):
    db = pymysql.connect("localhost","root","123456","user_trajectory")

    cursor = db.cursor()

    sql = """ SELECT * FROM beijing WHERE DEVICEID in (SELECT DEVICEID FROM beijing GROUP BY DEVICEID HAVING COUNT(DEVICEID)>%d) ORDER BY DEVICEID,`TIMESTAMP`
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

# rpc = fetch_rpc(10, timedelta(days=5))
# print(len(rpc))
# print(rpc)


