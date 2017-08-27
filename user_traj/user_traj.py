import pymysql
import util.geo_distance as geo
# import util.categ_distance as Categ
import util.GaoDe_api as Categ
from similiraty import similarity_dp
from RPC.rpc_find import fetch_rpc
from datetime import timedelta
import random
import _pickle as pickle

app_key_list = ["f209f1aaf086cea9ba1a17ddef79f4ee",
                "6ebdcf85286d28e8fbf552f8a6d8fab3",
                "eb5e44ec0a6c9ae043ce3a5e4f8e5c03",
                "602578e87e5a1d3df9f3fa223a58f92d",
                "87969ea0aeb53c72f6e7d8c59993e054",
                "4ac8b534f329ba0d7c3d3706dfb9a952",
                "5fad861f31c004537916393b002d95ae",
                "5ea7bd650a175d98015e7e005747a565",
                "90f1893b379d5c849be5022002520ddc",
                "12e8d95462259a1a32e785b1da97e4e9", ]


def get_traj(user):
    db = pymysql.connect("localhost", "root", "Meituan-0502", "user_trajectory")

    cursor = db.cursor()

    # user = '869736020272661_9492bc4826f4'
    sql = """ SELECT `TIMESTAMP`,LONGITUDE,LATITUDE FROM user_traj where DEVICEID='%s' ORDER BY `TIMESTAMP`
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
    for i in range(len(users_traj)):
        if geo.great_circle_distance(ls[1], ls[2], users_traj[i][1], users_traj[i][2]) < DT:
            le = users_traj[i]
        else:
            s = users_traj.index(ls)
            e = users_traj.index(le)
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
            ls = users_traj[i]
            le = users_traj[i]
    s = users_traj.index(ls)
    e = users_traj.index(le)
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
    sorted_list = []
    for i, user in enumerate(rpc_list):
        print("第%s个用户%s " % (i, user))
        user_traj = get_traj(user)
        stay_region_list = stay_regions(user_traj, dt, tt)
        catg_region, categ_locations = significance_score(stay_region_list, user_traj, threshold)
        cal = cal_similarity(user, catg_region, categ_locations)
        cal_list.append(cal)
    for i in range(len(cal_list)):
        sim_dict = {}
        for j in range(len(cal_list)):
            if i != j:
                item_dict = {}
                item_dict[cal_list[j]] = similarity_dp.g_lcss(cal_list[i], cal_list[j], time_span)
                sim_dict[cal_list[i]] = item_dict
                sorted_list.append(sim_dict)
    return sorted_list



rpc_list = fetch_rpc(10, timedelta(days=5))
r = cal_sim_result(rpc_list, 80, 10, 0.01, 3)
f = open('pickle_file', 'wb')
c = pickle.dump(r, f, True)
f.close()
print(r)

