import requests

def categ_distance(lat,lng):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    params = {'callback': 'renderReverse', 'posi': '0', 'output': 'json', 'batch': 'true', 'ak': '1NMP6Wn9BzUvDmpne0Gq0Xondt4IfTQg', 'extensions_poi':'null'}
    location = {'location': '%s,%s' % (lat,lng)}
    params.update(location)
    venues = requests.get(url=url,params=params).content

    return venues

venues = categ_distance(31.160439,108.411063)

print(venues)