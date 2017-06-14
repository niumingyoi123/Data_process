import numpy as np
import util.geo_distance as geo
import datetime

def g_lcss(tradj0, tradj1, timespan):
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

    t0 = tradj0['tradj']
    t1 = tradj1['tradj']
    n0 = len(t0)
    n1 = len(t1)

    C = [[0] * (n1+1) for _ in range(n0+1)]

    for i in range(1, n0+1):
        for j in range(1, n1+1):
            d = t0[i-1]['timestamp']-t1[j-1]['timestamp']
            if d.total_seconds() < timespan*60:
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



# t1 = {'deviceId': '357623050199296_d05785efdf4c', 'tradj': [{'timestamp': datetime.datetime(2016, 9, 1, 6, 50, 5), 'typecode': '060603'}, {'timestamp': datetime.datetime(2016, 9, 1, 6, 50, 5), 'typecode': '060603'}, {'timestamp': datetime.datetime(2016, 9, 1, 6, 50, 5), 'typecode': '060603'}]}
# t0 = {'deviceId': '869736020272661_9492bc4826f4', 'tradj': [{'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}, {'timestamp': datetime.datetime(2016, 9, 1, 5, 21, 45), 'typecode': '060000'}]}
#
# sim = g_lcss(t0,t1,3)
# print(sim)
