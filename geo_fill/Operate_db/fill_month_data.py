#coding:utf-8

import json,os,csv
import pickle


def load_geo2():
    with open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\pingan\\pingan.csv', newline='', encoding='utf-8',errors='ignore') as csvfile:
        reader = csv.reader(csvfile)

    # if os.path.exists('/Users/niumingyi/Documents/pingan.csv'):
    #     file_geo = open('/Users/niumingyi/Documents/pingan.csv', 'r')
    #     geo_file = file_geo.readlines()
    #     file_geo.close()
        geo_routmacs = {}
        try:
            for part in reader:
                # part = line.split(',')
                geo_routmac = {}
                geo_routmac[part[1]] = [part[3], part[4]]
                geo_routmacs[part[2]] = geo_routmac
        except:
            print(part)
    return geo_routmacs

def load_user2(geo_routmacs,d, file_object):
    load_user = {}
    with open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\wifi_list_smzapi003_2016120%s.json' % d, encoding='utf-8',
              errors='ignore') as Jsonfile:
        user_datas = Jsonfile.readlines()
        count = 0
        blank_num = 0
        count_0mac = 0
        # if not os.path.exists('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\geo_data'):
        #     file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\geo_data', 'x')
        # else:
        #     file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\geo_data', 'a')
        for user_data in user_datas:
            try:
                count += 1
                user_data_json = json.loads(user_data)
                timestamp = user_data_json['timestamp']
                deviceid = user_data_json['deviceid']
                wifi_lists = user_data_json['wifi_list']
                used = False
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
                        # file_object.write(json.dumps(load_user) + '\n')
                        pickle.dump(json.dumps(load_user) + '\n', file_object, True)
                        continue
                if used:
                    count_0mac += 1
            except:
                blank_num += 1
                print(count)
        print("空地理位置数据个数为: %d" % blank_num)
        print("路由为00:00:00:00:00:00 的行数为 ： %d" % count_0mac)



geo_routmacs = load_geo2()
# file_object = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\11.18-12.31\\geo_data', 'wb')
# for d in range(1, 10):
#     load_user2(geo_routmacs, d, file_object)
# file_object.close()
# f_sorted = open('sorted_list_300_30_week_2', 'wb')
# pickle.dump(sorted_list_300_30, f_sorted, True)
# f_sorted.close()