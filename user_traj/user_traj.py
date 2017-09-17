import pymysql
import util.geo_distance as geo
# import util.categ_distance as Categ
import util.GaoDe_api as Categ
from similiraty import similarity_dp
from RPC.rpc_find import fetch_rpc
import random
import _pickle as pickle
from datetime import timedelta
import datetime
import json
from util.date_encoder import DateEncoder

app_key_list = ["92dfa9b76e3506a58fb42499b5f660cb",
                "08a7e019c18c2f7d06ad4587f6e3bf4a",
                "426d773a348c1a193b2ad66437e9cb4f",
                "bf5d9acbe1efd70b6ac314033c07a378",
                "9635274dfd23e2f6811ee76bee1ef9e1",
                "16842e97ab134a01c8768068ba1a4a77",
                "7268279905d486ff92a4dcd723dfc4cd",
                "d9822af9d8215883ac586e685e179948",
                "9d61345b294abd54bcf869ac36d9ea1e",
                "7e73746735215c2f9308a54f425dab15",]

app_key_list_2 = ["66d50cdfc47cff0151b2c7d3d4462457",
                    "916bb8878e358ba1d6b967c9e129106e",
                    "245f194817f0979f3ba4ef577b54455b",
                    "59f833ce3dd9dbceb2a0babb8db79383",
                    "b8866288424f845eca5c81b79d32ca2a",
                    "5627ac77ee6d0184a68ee4ee2832ae9f",
                    "cd4ef00ad0f9618439f25bdaa08a1574",
                    "aaeecb30fc869bfd45ce3963f32f6c87",
                    "55050e99cfb328e8842210d3bcb4f2b4",
                    "18b8f8abf8aec5d2a89ef1ff46e6ea72",]

app_key_list_2 += app_key_list

def get_traj(user):
    db = pymysql.connect("localhost","root","Meituan-0502","user_trajectory")

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
        # if int((le[0] - ls[0]).total_seconds()) >= TT * 60:
        t_big = max(le[0], ls[0])
        t_small = min(le[0], ls[0])
        t_small += datetime.timedelta(days=(t_big-t_small).days)
        if le[0].weekday() == ls[0].weekday() and int((t_big-t_small).total_seconds()) >= TT * 60:
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
        catg = Categ.categ_distance(stay_region[0][2], stay_region[0][1], app_key_list_2[random.randint(0, 19)])[
            'typecode']
        categ_location = stay_region[0]
        for location in stay_region:
            l_score = score_in_tradj(users_traj, location) * score_in_region(stay_region, location)
            catg_dis = Categ.categ_distance(location[2], location[1], app_key_list_2[random.randint(0, 19)])
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
    # cal_list = []
    cal_list_file = open('cal_list_split_250_300_30', 'rb')
    cal_list = pickle.load(cal_list_file)
    for i, user in enumerate(rpc_list):
        if i <=250:
            continue
        print("第%s个用户%s " % (i, user))
        user_traj = get_traj(user)
        user_first = "%s_first" % user
        user_second = "%s_second" % user
        user_first_traj = user_traj[:int(len(user_traj)/2)]
        user_second_traj = user_traj[int(len(user_traj)/2):]
        # stay_region_list = stay_regions(user_traj, dt, tt)
        first_stay_region_list = stay_regions(user_first_traj, dt, tt)
        second_stay_region_list = stay_regions(user_second_traj, dt, tt)
        attempts = 0
        success = False

        while attempts < 3 and not success:
            try:
                catg_region_first, categ_locations_first = significance_score(first_stay_region_list, user_first_traj, threshold)
                success = True
            except:
                attempts += 1
                if attempts == 3:
                    break
                print("第%s个用户没有数据" % i)
                if i % 50 == 0:
                    f_err = open('cal_list_split_%s_%s_%s' % (i, dt, tt), 'wb')
                    pickle.dump(cal_list, f_err, True)
                    f_err.close()
            try:
                catg_region_second, categ_locations_second = significance_score(second_stay_region_list, user_second_traj, threshold)
                success = True
            except:
                attempts += 1
                if attempts == 3:
                    break
                print("第%s个用户没有数据" % i)
                if i % 50 == 0:
                    f_err = open('cal_list_split_%s_%s_%s' % (i, dt, tt), 'wb')
                    pickle.dump(cal_list, f_err, True)
                    f_err.close()
        cal_first = cal_similarity(user_first, catg_region_first, categ_locations_first)
        print(user_first)
        cal_list.append(cal_first)
        cal_second = cal_similarity(user_second, catg_region_second, categ_locations_second)
        print(user_second)
        cal_list.append(cal_second)
        if i % 50 == 0:
            f_succ = open('cal_list_split_%s_%s_%s' % (i, dt, tt), 'wb')
            pickle.dump(cal_list, f_succ, True)
            f_succ.close()
    f_cal = open('cal_list_split_%s_%s' % (dt, tt), 'wb')
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
                item_tuple = (recommend_id, similarity_dp.g_lcss(cal_list[i], cal_list[j], time_span)) # 计算时间
                # item_tuple = (recommend_id, similarity_dp.g_lcss_week(cal_list[i], cal_list[j])) # 计算week
                recommend_list.append(item_tuple)
        recommend_list.sort(key=lambda tup: tup[1], reverse=True)
        sim_dict[target_id] = recommend_list
        sorted_list.append(sim_dict)
    return sorted_list



# rpc_list = fetch_rpc(10, timedelta(days=5))
# r = cal_sim_result(rpc_list, 300, 30, 0.01, 3)
f = open('cal_list_split_300_30', 'rb')
cal_list_split_300_30 = pickle.load(f)
f.close()
# print(cal_list_split_300_30)
sorted_list_split_300_30_week = sorted_list_cal(cal_list_split_300_30, 3)
f_sorted = open('sorted_list_split_300_30', 'wb')
pickle.dump(sorted_list_split_300_30_week, f_sorted, True)
f_sorted.close()

# print(sorted_list_split_300_30_week)
# f = open('sorted_list_300_30', 'rb')
# sorted_list_300_30 = pickle.load(f)
# f.close()
# print(sorted_list_300_30)


# user = "352419061869927_608F5C35E1D0"
# dt = 80
# tt = 10
# user_traj = get_traj(user)
# print(user_traj)
# stay_region_list = stay_regions(user_traj, dt, tt)
# print(stay_region_list)

