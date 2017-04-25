import pymysql
import util.geo_distance as geo

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

users_traj = get_traj()
stay_regions = stay_regions(users_traj,80,10)
print(len(stay_regions))