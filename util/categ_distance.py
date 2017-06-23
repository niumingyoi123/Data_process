import foursquare


def categ_distance(lat,lng):
    # Construct the client object
    client = foursquare.Foursquare(client_id='RYYHLSVLTPNBS4U4JK3NJU0TYDPQ4CY3BDII2P2WCFJ3Y2PW',
                                   client_secret='MS4JK4VAFLY4FYY4IE23WXHKHTFOYKW1A4XPZUKKAWQ3ZUAS')
    # venue = client.venues('40a55d80f964a52020f31ee3')
    venue = client.venues.explore(params={'ll': '%s,%s'%(lat,lng), 'limit': '1'})

    venues = venue['groups'][0]['items'][0]['venue']

    # print(venues)

    venue_detail = {}

    venue_detail['name'] = venues['name']
    venue_detail['distance'] = venues['location']['distance']
    venue_detail['categories'] = venues['categories'][0]['name']

    print(venue_detail)

    return venue_detail['distance'],venue_detail['categories']