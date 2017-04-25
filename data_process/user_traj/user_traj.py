import pymysql
import util.geo_distance as geo
# import util.categ_distance as Categ
import util.BaiduMap_api as Categ

def get_traj():
    db = pymysql.connect("localhost", "root", "", "user_trajectory")

    cursor = db.cursor()

    user = '869736020272661_9492bc4826f4'
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
    for stay_region in stay_regions:
        max_score = 0
        catg = Categ.categ_distance(stay_region[0][2],stay_region[0][1])[1]
        for location in stay_region:
            l_score = score_in_tradj(users_traj,location)*score_in_region(stay_region,location)
            catg_dis = Categ.categ_distance(location[2],location[1])
            if l_score > ST and (l_score/catg_dis[0]) > max_score:
                max_score = l_score/catg_dis[0]
                catg = catg_dis[1]
        if max_score > 0:
            catg_region.append(catg)
    return catg_region

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


users_traj = get_traj()
stay_regions = stay_regions(users_traj,80,10)
# print(stay_regions)

catg_region = significance_score(stay_regions,users_traj,0.01)
print(catg_region)