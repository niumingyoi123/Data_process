import requests

def categ_distance(lat,lng):
    url = 'http://api.map.baidu.com/place/v2/search'
    params = {'query': '饭店', 'scope': '2', 'radius': '2000', 'output': 'json', 'ak': '1NMP6Wn9BzUvDmpne0Gq0Xondt4IfTQg','page_size':'1'}
    location = {'location': '%s,%s' % (lat,lng)}
    params.update(location)
    venues = requests.get(url=url,params=params).json()['results'][0]


    venue_detail = {}

    venue_detail['name'] = venues['name']
    venue_detail['distance'] = venues['detail_info']['distance']
    venue_detail['categories'] = venues['detail_info']['tag']

    print(venue_detail)

    return venue_detail['distance'],venue_detail['categories']

# categ_distance(31.160439,108.411063)