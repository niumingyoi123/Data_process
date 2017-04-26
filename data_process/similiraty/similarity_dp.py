import numpy as np
import util.geo_distance as geo

def g_lcss(t0, t1, timespan):
    """
    Usage
    -----
    The Longuest-Common-Subsequence distance between trajectory t0 and t1.

    Parameters
    ----------
    param tradj0 : {"deviceId":"deviceId","tradj":[{"timestamp":"timestamp","typecode":"typecode"},]}
    t0 = tradj0["tradj"]
    param tradj1 : {"deviceId":"deviceId","tradj":[{"timestamp":"timestamp","typecode":"typecode"},]}
    t1 = tradj1["tradj"]
    timespan : time span

    Returns
    -------
    lcss : float
           The Longuest-Common-Subsequence distance between trajectory t0 and t1
    """
    # n0 = len(t0)
    # n1 = len(t1)
    # # An (m+1) times (n+1) matrix
    # C = [[0] * (n1+1) for _ in range(n0+1)]
    # for i in range(1, n0+1):
    #     for j in range(1, n1+1):
    #         if geo.great_circle_distance(t0[i-1,0],t0[i-1,1],t1[j-1,0],t1[j-1,1])<eps:
    #             C[i][j] = C[i-1][j-1] + 1
    #         else:
    #             C[i][j] = max(C[i][j-1], C[i-1][j])
    # lcss = 1-float(C[n0][n1])/min([n0,n1])


    n0 = len(t0)
    n1 = len(t1)

    C = [[0] * (n1+1) for _ in range(n0+1)]

    for i in range(1, n0+1):
        for j in range(1, n1+1):
            if t0[i-1]['timestamp']-t1[j-1]['timestamp'] < timespan:
                C[i][j] = C[i-1][j-1]+score_type(t0[i-1]['typecode'],t1[j-1]['typecode'])
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    lcss = 1-float(C[n0][n1])/min([n0,n1])

    return lcss

def score_type(type_code1,type_code2):
    if type_code1 == type_code2:
        return 1
    elif type_code1[:4] == type_code2[:4]:
        return 0.8
    elif type_code1[:2] == type_code2[:2]:
        return 0.5
    else:
        return 0


traj_A = np.array([[-122.39534, 37.77678],[-122.3992 , 37.77631],[-122.40235, 37.77594],[-122.40553, 37.77848],
                   [-122.40801, 37.78043],[-122.40837, 37.78066],[-122.41103, 37.78463],[-122.41207, 37.78954],
                   [-122.41252, 37.79232],[-122.41316, 37.7951 ],[-122.41392, 37.7989 ],[-122.41435, 37.80129],
                   [-122.41434, 37.80129]])
traj_B = np.array([[-122.39472, 37.77672],[-122.3946 , 37.77679],[-122.39314, 37.77846],[-122.39566, 37.78113],
                   [-122.39978, 37.78438],[-122.40301, 37.78708],[-122.4048 , 37.78666],[-122.40584, 37.78564],
                   [-122.40826, 37.78385],[-122.41061, 37.78321],[-122.41252, 37.78299]])

lcss = g_lcss(traj_A,traj_B,100)

print(lcss)