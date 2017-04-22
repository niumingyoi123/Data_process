# _*_coding:utf-8_*_

import os
import json
import codecs

class filling:
    def load_geo(self):

        if os.path.exists('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_1'):
            file_geo = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_1','r')
            geo_file=file_geo.readlines()
            file_geo.close()
            result=[]
            for line in geo_file:
                mac_geo = {}
                try:
                    part = line.split(',')
                    mac_geo["ssid"] = part[1]
                    mac_geo["routemac"]=part[2]
                    mac_geo["longitude"]=part[3]
                    mac_geo["latitude"]=part[4]
                    result.append(mac_geo)
                except:
                    print(len(mac_geo))
        else:
            print('File Not Found')

        return result

    def load_geo2(self):
        if os.path.exists('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_1'):
            file_geo = open('F:\\毕设\\毕设参考\\数据集\\wifi数据集\\201606\\pingan\\part_1','r')
            geo_file=file_geo.readlines()
            file_geo.close()
            geo_routmacs = {}
            for line in geo_file:
                part = line.split(',')
                geo_routmac={}
                geo_routmac[part[1]]=[part[3],part[4]]
                geo_routmacs[part[2]]=geo_routmac
        return geo_routmacs

    def load_user(self,mac_geo):
        load_user = {}
        user_datas_file = codecs.open(
            'F:\\毕设\\毕设参考\\数据集\\wifi数据集\\20160905\\wifi_list_smzapi001_smzapi001_20160901.json', 'r', 'utf-8', 'ignore')
        user_datas = user_datas_file.readlines()
        user_datas_file.close()
        count = 0
        file_object = open('f:/new_geo_data_1', 'a')
        for user_data in user_datas:
            try:
                count += 1
                user_data_json = json.loads(user_data)
                timestamp = user_data_json['timestamp']
                deviceid = user_data_json['deviceid']
                wifi_lists = user_data_json['wifi_list']
                for wifi_info in wifi_lists:
                    wifi_ssid = wifi_info['ssid']
                    wifi_mac = wifi_info['routemac']
                    for geo_data in mac_geo:
                        # if wifi_mac == geo_data['routemac'] and wifi_ssid == geo_data['ssid']:
                        if wifi_mac in geo_data['routemac'] and wifi_ssid in geo_data['ssid']:
                            load_user['timestamp'] = timestamp
                            load_user['deviceid'] = deviceid
                            load_user['longitude'] = geo_data['longitude']
                            load_user['latitude'] = geo_data['latitude']
                file_object.write(str(load_user) + '\n')
            except:
                print(count)
        file_object.close()

    def load_user2(self,geo_routmacs):
        load_user = {}
        user_datas_file = codecs.open(
            'F:\\毕设\\毕设参考\\数据集\\wifi数据集\\20160905\\wifi_list_smzapi001_smzapi001_20160901.json', 'r', 'utf-8', 'ignore')
        user_datas = user_datas_file.readlines()
        user_datas_file.close()
        count=0
        file_object = open('f:/new_geo_data_2', 'a')
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
                           file_object.write(str(load_user) + '\n')
            except:
                print(count)


    # def __init__(self):
    #     # mac_geo = self.load_geo()
    #     # self.load_user(mac_geo)
    #     load_geo2 = self.load_geo2()
    #     self.load_user2(load_geo2)
