import requests
from geojson import Polygon
from geojson import Point
from geojson_utils import point_in_polygon
import json

url = "http://restapi.amap.com/v3/config/district?keywords=东城区&subdistrict=0&key=5ea7bd650a175d98015e7e005747a565&showbiz=false&extensions=all&output=JSON"

response = requests.get(url).json()

polyline = response['districts'][0]['polyline']

# print(response)

# print(polyline)

# print(type(polyline))

polyline = polyline.split(";")
polylines = []
for ps in polyline:
    item = ps.split(",")
    p = [float(x) for x in item]
    polylines.append(p)
print(polylines)

def pt_in_poly(polylines, lng, lat):
    ncross = 0
    poly_size = len(polylines)
    for i in range(poly_size):
        poly_first = polylines[i]
        poly_second = polylines[(i+1)%poly_size]
        if poly_first[0] == poly_second[0]:
            continue
        if lng < max((poly_first[0]),(poly_second[0])):
            continue
        if lng >= max((poly_first[0]),(poly_second[0])):
            continue
        poly_x = ((lng - (poly_first[0]))*((poly_second[1])-(poly_first[1])))/\
                 ((poly_second[0])-(poly_first[0]))+(poly_first[1])
        if poly_x > lat:
            ncross+=1
    return ncross%2 ==1

# flag = pt_in_poly(polylines,116.387663,39.960923)
# print(flag)

polygon = Polygon([polylines])
point = Point((116.387663,39.960923))
print(polygon)
print(point)
print(type(point))
print(point_in_polygon(point,polygon))
# in_str = '{"type": "Point", "coordinates": [5, 5]}'
# out_str = '{"type": "Point", "coordinates": [15, 15]}'
# box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
# in_box = json.loads(in_str)
# out_box = json.loads(out_str)
# box = json.loads(box_str)
#
# print(point_in_polygon(in_box, box))
#True
# point_in_polygon(out_box, box)
#False