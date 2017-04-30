import requests


def categ_distance(lat,lng):
    url = 'http://restapi.amap.com/v3/place/around?key=90f1893b379d5c849be5022002520ddc&location=%s,%s&output=json&sortrule=distance&offset=20&types=05|06|07'%(lat,lng)

    response = requests.get(url).json()

    print(response['pois'])

    venues = response['pois'][0]


    venue_detail = {}

    venue_detail['name'] = venues['name']
    venue_detail['distance'] = venues['distance']
    venue_detail['typecode'] = venues['typecode']

    print(venue_detail)


    return float(venue_detail['distance']),venue_detail['typecode']

categ_distance(31.160439,108.411063)


