import pymysql
import util.geo_distance as geo
# import util.categ_distance as Categ
import util.GaoDe_api as Categ
from similiraty import similarity_dp
from RPC.rpc_find import get_traj_rpc
from datetime import timedelta

def get_traj(user):
    db = pymysql.connect("localhost", "root", "", "user_trajectory")

    cursor = db.cursor()

    # user = '869736020272661_9492bc4826f4'
    sql = """ SELECT `TIMESTAMP`,LONGITUDE,LATITUDE FROM dongcheng where DEVICEID='%s' ORDER BY `TIMESTAMP`
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

def stay_regions(users_traj,DT,TT):
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
        if geo.great_circle_distance(ls[1],ls[2],users_traj[i][1],users_traj[i][2])<DT:
            le = users_traj[i]
        else:
            s = users_traj.index(ls)
            e = users_traj.index(le)
            if int((le[0]-ls[0]).total_seconds()) >= TT*60:
                stay_region = []
                for i in range(s,e+1):
                    stay_region.append(users_traj[i])
                stay_regions.append(stay_region)
            else:
                for i in range(s,e+1):
                    stay_region=[]
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

def significance_score(stay_regions,users_traj,ST):
    catg_region = []
    categ_locations = []
    for stay_region in stay_regions:
        max_score = 0
        catg = Categ.categ_distance(stay_region[0][2],stay_region[0][1])['typecode']
        categ_location = stay_region[0]
        for location in stay_region:
            l_score = score_in_tradj(users_traj,location)*score_in_region(stay_region,location)
            catg_dis = Categ.categ_distance(location[2],location[1])
            if l_score > ST and (l_score/catg_dis['distance']) > max_score:
                max_score = l_score/catg_dis['distance']
                catg = catg_dis['typecode']
                categ_location = location
        if max_score > 0:
            catg_region.append(catg)
            categ_locations.append(categ_location)
    return catg_region,categ_locations

def score_in_region(stay_region,target_location):
    count = 0
    for location in stay_region:
        if location[1] == target_location[1] and location[2] == target_location[2]:
            count+=1
    return count/len(stay_region)

def score_in_tradj(users_traj,target_location):
    count = 0
    for user_traj in users_traj:
        if user_traj[1] == target_location[1] and user_traj[2] == target_location[2]:
            count+=1
    return count/len(users_traj)

def cal_similarity(user,catg_region,categ_locations):
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

rpc = get_traj_rpc(10,timedelta(days=5))
print(rpc)

cal_list = []

for user in rpc:
    users_traj = get_traj(user)
    print(users_traj)
    user_stay_regions = stay_regions(users_traj,80,10)
    print(user_stay_regions)
    catg_region, categ_locations = significance_score(user_stay_regions, users_traj, 0.01)
    print(catg_region)
    print(categ_locations)
    cal = cal_similarity(user,catg_region,categ_locations)
    print(cal)
    cal_list.append(cal)
    print(cal_list)
l_cal = len(cal_list)
res = []

for n in range(l_cal):
    for m in range(l_cal):
        if n==m:
            continue
        else:
            sim = similarity_dp.g_lcss(cal_list[m],cal_list[n],3)
            res.append(sim)

print(res)
# sim = similarity_dp.g_lcss(cal1,cal2,3)


# user1 = '869736020272661_9492bc4826f4'
# users_traj1 = get_traj(user1)
# print("users_traj1  "+str(users_traj1))
# stay_regions1 = stay_regions(users_traj1,80,10)
# print("stay_regions1  "+str(stay_regions1))
#
# catg_region1,categ_locations1 = significance_score(stay_regions1,users_traj1,0.01)
# print("catg_region1  "+str(catg_region1))
# print("categ_locations1  "+str(categ_locations1))
# print(len((catg_region1)))
# print(len((categ_locations1)))
# cal1 = cal_similarity(user1,catg_region1,categ_locations1)
# print("cal1  "+str(cal1))
#
# user2 = '357623050199296_d05785efdf4c'
# users_traj2 = get_traj(user2)
# print("users_traj2  "+str(users_traj2))
# stay_regions2 = stay_regions(users_traj2,80,10)
# print("stay_regions2  "+str(stay_regions2))
#
# catg_region2,categ_locations2 = significance_score(stay_regions2,users_traj2,0.01)
# print("catg_region2  "+str(catg_region2))
# print("categ_locations2  "+str(categ_locations2))
# print(len((catg_region2)))
# print(len((categ_locations2)))
# cal2 = cal_similarity(user2,catg_region2,categ_locations2)
# print("cal2  "+str(cal2))

# sim = similarity_dp.g_lcss(cal1,cal2,3)
# print("sim  "+str(sim))



