import requests
import util.geo_distance as geo

def categ_distance(lat,lng):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s,%s&rankby=distance&key=AIzaSyA8iZ8gpSf5tzTF_Hu8NJrTvsIfn_VZHNQ'%(lat,lng)

    response = requests.get(url).json()

    venues = response['results'][0]

    # venue_detail = {}
    #
    # venue_detail['name'] = venues['name']
    # venue_detail['distance'] = venues['detail_info']['distance']
    # venue_detail['categories'] = venues['detail_info']['tag']

    print(venues)

    # return venue_detail['distance'],venue_detail['categories']

categ_distance(31.160439,108.411063)


