import requests
from geojson import Polygon

app_key_list = ["f209f1aaf086cea9ba1a17ddef79f4ee",
                "6ebdcf85286d28e8fbf552f8a6d8fab3",
                "eb5e44ec0a6c9ae043ce3a5e4f8e5c03",
                "602578e87e5a1d3df9f3fa223a58f92d",
                "602578e87e5a1d3df9f3fa223a58f92d",
                "4ac8b534f329ba0d7c3d3706dfb9a952",
                "5fad861f31c004537916393b002d95ae",
                "5ea7bd650a175d98015e7e005747a565",
                "90f1893b379d5c849be5022002520ddc",
                "12e8d95462259a1a32e785b1da97e4e9", ]


def categ_distance(lat, lng, app_key):
    url = 'http://restapi.amap.com/v3/place/around?key=%s&location=%s,%s&output=json&sortrule=distance&offset=20&types=05|06|07' % (
        app_key, lat, lng)

    response = requests.get(url).json()

    # print(response)

    venues = response['pois'][0]
    # print(venues)

    venue_detail = {}

    venue_detail['id'] = venues['id']
    venue_detail['distance'] = float(venues['distance'])
    venue_detail['typecode'] = venues['typecode']

    # print(venue_detail)


    # return float(venue_detail['distance']),venue_detail['typecode']
    return venue_detail


# categ_distance(31.160439,108.411063)

def districts_filter(district):
    url = "http://restapi.amap.com/v3/config/district?keywords=%s&subdistrict=0&key=5ea7bd650a175d98015e7e005747a565&showbiz=false&extensions=all&output=JSON" % district

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
