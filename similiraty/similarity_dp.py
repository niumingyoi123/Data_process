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

    if n0 == 0 or n1 == 0 :
        return 0

    C = [[0] * (n1+1) for _ in range(n0+1)]

    for i in range(1, n0+1):
        for j in range(1, n1+1):
            d = t0[i-1]['timestamp']-t1[j-1]['timestamp']
            if abs(d.total_seconds()) < timespan*3600:
                C[i][j] = C[i-1][j-1]+score_type(t0[i-1]['typecode'],t1[j-1]['typecode'])
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    lcss = float(C[n0][n1])/((n0+n1)/2)

    return lcss

def g_lcss_week(tradj0, tradj1):
    t0 = tradj0['tradj']
    t1 = tradj1['tradj']
    n0 = len(t0)
    n1 = len(t1)

    if n0 == 0 or n1 == 0 :
        return 0

    C = [[0] * (n1+1) for _ in range(n0+1)]

    for i in range(1, n0+1):
        for j in range(1, n1+1):
            week1 = t0[i-1]['timestamp'].date().weekday()
            week2 = t1[j-1]['timestamp'].date().weekday()
            if week1 == week2:
                C[i][j] = C[i-1][j-1]+score_type(t0[i-1]['typecode'],t1[j-1]['typecode'])
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    lcss = float(C[n0][n1])/((n0+n1)/2)

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


# tradj0 = {'deviceId': 'A100003A5C0901_6c25b97aceaa_first', 'tradj': [{'timestamp': datetime.datetime(2016, 8, 1, 16, 40, 17), 'typecode': '050102'}]}
# tradj1 = {'deviceId': 'A100003A5C0901_6c25b97aceaa_second', 'tradj': [{'timestamp': datetime.datetime(2016, 8, 2, 2, 30, 15), 'typecode': '050102'}, {'timestamp': datetime.datetime(2016, 8, 2, 6, 40, 12), 'typecode': '050000'}, {'timestamp': datetime.datetime(2016, 8, 2, 7, 10, 6), 'typecode': '061210'}, {'timestamp': datetime.datetime(2016, 8, 2, 7, 30, 12), 'typecode': '050100'}, {'timestamp': datetime.datetime(2016, 8, 6, 22, 10, 17), 'typecode': '050102'}]}



# pre = g_lcss(tradj0, tradj1, 3)

# print(pre)