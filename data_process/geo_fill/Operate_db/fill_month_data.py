#coding:utf-8

import json,os

def load_geo2(i):
    if os.path.exists('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_%d' % i):
        file_geo = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_%d' % i, 'r')
        geo_file = file_geo.readlines()
        file_geo.close()
        geo_routmacs = {}
        try:
            for line in geo_file:
                part = line.split(',')
                geo_routmac = {}
                geo_routmac[part[1]] = [part[3], part[4]]
                geo_routmacs[part[2]] = geo_routmac
        except:
            print(line)
    return geo_routmacs

def load_user2(geo_routmacs,d):
    load_user = {}
    with open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\wifi_list_smzapi003_201610%d.json' % d, encoding='utf-8',
              errors='ignore') as Jsonfile:
        user_datas = Jsonfile.readlines()
        count = 0
        blank_num = 0
        count_0mac = 0
        if not os.path.exists('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\geo_data_%d'%d):
            file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\geo_data_%d'%d, 'x')
        else:
            file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\geo_data_%d'%d, 'a')
        # file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\10.17-11.17\\geo_data', 'a')
        for user_data in user_datas:
            try:
                count += 1
                user_data_json = json.loads(user_data)
                timestamp = user_data_json['timestamp']
                deviceid = user_data_json['deviceid']
                wifi_lists = user_data_json['wifi_list']
                used = False;
                for wifi_list in wifi_lists:
                    routemac = wifi_list['routemac']
                    if routemac == '00:00:00:00:00:00':
                        used = True
                    if routemac in geo_routmacs.keys():
                        ssid_geo = wifi_list['ssid']
                        # if ssid_geo in geo_routmacs[routemac].keys():
                        load_user['timestamp'] = timestamp
                        load_user['deviceid'] = deviceid
                        load_user['longitude'] = geo_routmacs[routemac][ssid_geo][0]
                        load_user['latitude'] = geo_routmacs[routemac][ssid_geo][1]
                        file_object.write(json.dumps(load_user) + '\n')
                        continue
                if used:
                    count_0mac += 1
            except:
                blank_num += 1
                print(count)
        print("空地理位置数据个数为: %d" % blank_num)
        print("路由为00:00:00:00:00:00 的行数为 ： %d" % count_0mac)



for i in range(1,9):
    geo_routmacs = load_geo2(i)
    for d in range(17,32):
        load_user2(geo_routmacs,d)
