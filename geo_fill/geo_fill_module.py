# _*_coding:utf-8_*_

import os
import json, csv
import codecs


filepath = '/Users/niumingyi/Documents/pingan.csv'
def load_geo2():
    with open(filepath,  newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader((line.replace('\0', '') for line in csvfile))

    # with open(filepath, newline='', encoding='utf-8', errors='ignore') as csvfile:
    #     reader = csv.reader(csvfile)
        geo_routmacs = {}
        for line in reader:
            try:
                geo_routmac = {}
                geo_routmac[line[1]] = [line[3], line[4]]
                geo_routmacs[line[2]] = geo_routmac
            except:
                print(line)
    return geo_routmacs


def load_user2(geo_routmacs,d):
    load_user = {}
    user_datas_file = codecs.open(
            '/Users/niumingyi/Downloads/data/%s.json' % d, 'r', 'utf-8', 'ignore')
    user_datas = user_datas_file.readlines()
    user_datas_file.close()
    count=0
    blank_num=0
    file_object = open('/Users/niumingyi/Downloads/data/new_geo_data', 'a')
    for user_data in user_datas:
        try:
            count+=1
            user_data_json = json.loads(user_data)
            timestamp = user_data_json['timestamp']
            deviceid = user_data_json['deviceid']
            wifi_lists = user_data_json['wifi_list']
            for wifi_list in wifi_lists:
                routemac = wifi_list['routemac']
                if routemac in geo_routmacs.keys():
                    ssid_geo = wifi_list['ssid']
                    if ssid_geo in geo_routmacs[routemac].keys():
                        load_user['timestamp'] = timestamp
                        load_user['deviceid'] = deviceid
                        load_user['longitude'] = geo_routmacs[routemac][ssid_geo][0]
                        load_user['latitude'] = geo_routmacs[routemac][ssid_geo][1]
                        file_object.write(json.dumps(load_user) + '\n')
                        break
        except:
            blank_num+=1
            print(count)
    print("空地理位置数据个数为: %d" %blank_num)