import requests
from geojson import Polygon


def categ_distance(lat,lng):
    url = 'http://restapi.amap.com/v3/place/around?key=5ea7bd650a175d98015e7e005747a565&location=%s,%s&output=json&sortrule=distance&offset=20&types=05|06|07'%(lat,lng)

    response = requests.get(url).json()

    print(response)

    venues = response['pois'][0]
    print(venues)

    venue_detail = {}

    venue_detail['id'] = venues['id']
    venue_detail['distance'] = float(venues['distance'])
    venue_detail['typecode'] = venues['typecode']


    # print(venue_detail)


    # return float(venue_detail['distance']),venue_detail['typecode']
    return venue_detail

# categ_distance(31.160439,108.411063)

def districts_filter(district):
    url = "http://restapi.amap.com/v3/config/district?keywords=%s&subdistrict=0&key=5ea7bd650a175d98015e7e005747a565&showbiz=false&extensions=all&output=JSON"%district

    response = requests.get(url).json()

    polyline = response['districts'][0]['polyline']

    polyline = polyline.split(";")
    polylines = []
    for ps in polyline:
        item = ps.split(",")
        p = [float(x) for x in item]
        polylines.append(p)
    # print(polylines)
    polygon = Polygon([polylines])
    return polygon

