import pymysql
import util.geo_distance as geo
# import util.categ_distance as Categ
import util.GaoDe_api as Categ
from similiraty import similarity_dp
from RPC.rpc_find import fetch_rpc
from datetime import timedelta
import random
import _pickle as pickle
import json
from util.date_encoder import DateEncoder

app_key_list = ["52c469b8f1f26f14c28576d2d4b6e87c",
                "ffc6fead741c315a8cc4876e07bab825",
                "5cee07ef7640065cb182e870da66c7e1",
                "e908e95d55dba5c8ec0089ddf5dc26e9",
                "aa6783184da566114a4365c76e6a90ec",
                "7ee9abe8c41894e05a825016661d5910",
                "8c7f2f9d4607e4de174bf7e703f86de2",
                "36a95e53e2977825875b968ad1f73238",
                "5c95eeb4c28e0e0bfefd182eda0b2b35",
                "51444c5064e6501a308290f433feff30", ]


def get_traj(user):
    db = pymysql.connect("localhost", "root", "Meituan-0502", "user_trajectory")

    cursor = db.cursor()

    # user = '869736020272661_9492bc4826f4'
    sql = """ SELECT `TIMESTAMP`,LONGITUDE,LATITUDE FROM beijing where DEVICEID='%s' ORDER BY `TIMESTAMP`
    """ % user
    users_traj = []
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            user = []
            user.extend(row)
            users_traj.append(user)
    except:
        print("Error : unable to fetch data")
    return users_traj


def stay_regions(users_traj, DT, TT):
    """
    :param users_traj: user trajectory
    :param DT: distance threshold
    :param TT: time threshold
    :return: stay regions list
    """
    stay_regions = []
    ls = users_traj[0]
    le = users_traj[0]
    p = 1
    while p < len(users_traj):
        while p < len(users_traj) and geo.great_circle_distance(ls[1], ls[2], users_traj[p][1], users_traj[p][2]) < DT:
            le = users_traj[p]
            p = p + 1
        if p == len(users_traj):
            break
        s = users_traj.index(ls)
        e = p-1
        if int((le[0] - ls[0]).total_seconds()) >= TT * 60:
            stay_region = []
            for i in range(s, e + 1):
                stay_region.append(users_traj[i])
            stay_regions.append(stay_region)
        else:
            for i in range(s, e + 1):
                stay_region = []
                stay_region.append(users_traj[i])
                stay_regions.append(stay_region)
        p = e+1
        ls = users_traj[p]
        le = users_traj[p]
        p = p+1
    s = users_traj.index(ls)
    e = p-1
    stay_region = []
    for i in range(s, e + 1):
        stay_region.append(users_traj[i])
    stay_regions.append(stay_region)
    return stay_regions


def significance_score(stay_regions, users_traj, ST):
    catg_region = []
    categ_locations = []
    for stay_region in stay_regions:
        max_score = 0
        catg = Categ.categ_distance(stay_region[0][2], stay_region[0][1], app_key_list[random.randint(0, 9)])[
            'typecode']
        categ_location = stay_region[0]
        for location in stay_region:
            l_score = score_in_tradj(users_traj, location) * score_in_region(stay_region, location)
            catg_dis = Categ.categ_distance(location[2], location[1], app_key_list[random.randint(0, 9)])
            if l_score > ST and (l_score / catg_dis['distance']) > max_score:
                max_score = l_score / catg_dis['distance']
                catg = catg_dis['typecode']
                categ_location = location
        if max_score > 0:
            catg_region.append(catg)
            categ_locations.append(categ_location)
    return catg_region, categ_locations


def score_in_region(stay_region, target_location):
    count = 0
    for location in stay_region:
        if location[1] == target_location[1] and location[2] == target_location[2]:
            count += 1
    return count / len(stay_region)


def score_in_tradj(users_traj, target_location):
    count = 0
    for user_traj in users_traj:
        if user_traj[1] == target_location[1] and user_traj[2] == target_location[2]:
            count += 1
    return count / len(users_traj)


def cal_similarity(user, catg_region, categ_locations):
    tradjs = {}
    tradjs['deviceId'] = user
    temp_list = []
    for i in range(len(categ_locations)):
        tradj = {}
        tradj['timestamp'] = categ_locations[i][0]
        tradj['typecode'] = catg_region[i]
        temp_list.append(tradj)
    tradjs['tradj'] = temp_list
    return tradjs


def cal_sim_result(rpc_list, dt, tt, threshold, time_span):
    cal_list = []
    for i, user in enumerate(rpc_list):
        print("第%s个用户%s " % (i, user))
        user_traj = get_traj(user)
        stay_region_list = stay_regions(user_traj, dt, tt)
        try:
            catg_region, categ_locations = significance_score(stay_region_list, user_traj, threshold)
        except:
            print("第%s个用户没有数据" % i)
            if i % 50 == 0:
                f_err = open('cal_list_%s' % i, 'wb')
                pickle.dump(cal_list, f_err, True)
                f_err.close()
            continue
        cal = cal_similarity(user, catg_region, categ_locations)
        cal_list.append(cal)
        if i % 50 == 0:
            f_succ = open('cal_list_%s' % i, 'wb')
            pickle.dump(cal_list, f_succ, True)
            f_succ.close()
    f_cal = open('cal_list', 'wb')
    pickle.dump(cal_list, f_cal, True)
    f_cal.close()
    return cal_list

def sorted_list_cal(cal_list, time_span):
    sorted_list = []
    for i in range(len(cal_list)):
        sim_dict = {}
        target_id = cal_list[i]['deviceId']
        recommend_list = []
        for j in range(len(cal_list)):
            if i != j:
                recommend_id = cal_list[j]['deviceId']
                item_tuple = (recommend_id, similarity_dp.g_lcss(cal_list[i], cal_list[j], time_span))
                recommend_list.append(item_tuple)
        recommend_list.sort(key=lambda tup: tup[1], reverse=True)
        sim_dict[target_id] = recommend_list
        sorted_list.append(sim_dict)
    return sorted_list



# rpc_list = fetch_rpc(10, timedelta(days=5))
# r = cal_sim_result(rpc_list, 80, 10, 0.01, 3)
f = open('cal_list', 'rb')
cal_list = pickle.load(f)
f.close()
print(cal_list)
sorted_list = sorted_list_cal(cal_list, 3)
f_sorted = open('sorted_list', 'wb')
pickle.dump(sorted_list, f_sorted, True)
f_sorted.close()

print(sorted_list)

# user = "352419061869927_608F5C35E1D0"
# dt = 80
# tt = 10
# user_traj = get_traj(user)
# print(user_traj)
# stay_region_list = stay_regions(user_traj, dt, tt)
# print(stay_region_list)

