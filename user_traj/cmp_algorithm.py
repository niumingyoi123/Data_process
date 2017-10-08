from util.geo_distance import great_circle_distance
import numpy as np
import pickle

def g_lcss(t0, t1,eps):

    n0 = len(t0)
    n1 = len(t1)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n1+1) for _ in range(n0+1)]
    for i in range(1, n0+1):
        for j in range(1, n1+1):
            if great_circle_distance(t0[i-1,0],t0[i-1,1],t1[j-1,0],t1[j-1,1])<eps:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    lcss = 1-float(C[n0][n1])/min([n0,n1])
    return lcss


def g_edr(t0, t1, eps):
    n0 = len(t0)
    n1 = len(t1)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n1+1) for _ in range(n0+1)]
    for i in range(1, n0+1):
        for j in range(1, n1+1):
            if great_circle_distance(t0[i-1][0],t0[i-1][1],t1[j-1][0],t1[j-1][1])<eps:
                subcost = 0
            else:
                subcost = 1
            C[i][j] = min(C[i][j-1]+1, C[i-1][j]+1,C[i-1][j-1]+subcost)
    edr = float(C[n0][n1])/max([n0,n1])
    return edr


def g_dtw(t0,t1):

    n0 = len(t0)
    n1 = len(t1)
    C=np.zeros((n0+1,n1+1))
    C[1:,0]=float('inf')
    C[0,1:]=float('inf')
    for i in np.arange(n0)+1:
        for j in np.arange(n1)+1:
            C[i,j]=great_circle_distance(t0[i-1][0],t0[i-1][1],t1[j-1][0],t1[j-1][1]) +\
                   min(C[i,j-1],C[i-1,j-1],C[i-1,j])
    dtw = C[n0,n1]
    return dtw

def cmp_dtw_sorted_list_cal(cal_list):
    sorted_list = []
    for origin_k, origin_v in cal_list.items():
        sim_dict = {}
        target_id = origin_k
        recommend_list = []
        for target_k, target_v  in cal_list.items():
            if target_k != origin_k:
                recommend_id = target_k
                item_tuple = (recommend_id, g_dtw(origin_v, target_v)) # 计算时间
                # item_tuple = (recommend_id, similarity_dp.g_lcss_week(cal_list[i], cal_list[j])) # 计算week
                recommend_list.append(item_tuple)
        recommend_list.sort(key=lambda tup: tup[1], reverse=True)
        sim_dict[target_id] = recommend_list
        sorted_list.append(sim_dict)
    return sorted_list

def cmp_edr_sorted_list_cal(cal_list, eps):
    sorted_list = []
    for origin_k, origin_v in cal_list.items():
        sim_dict = {}
        target_id = origin_k
        recommend_list = []
        for target_k, target_v  in cal_list.items():
            if target_k != origin_k:
                recommend_id = target_k
                item_tuple = (recommend_id, g_edr(origin_v, target_v, eps)) # 计算时间
                # item_tuple = (recommend_id, similarity_dp.g_lcss_week(cal_list[i], cal_list[j])) # 计算week
                recommend_list.append(item_tuple)
        recommend_list.sort(key=lambda tup: tup[1], reverse=True)
        sim_dict[target_id] = recommend_list
        sorted_list.append(sim_dict)
    return sorted_list



f = open('cal_list_cmp', 'rb')
cal_list_cmp = pickle.load(f)
f.close()
# print(cal_list_split_300_30)
sorted_dtw_list_split_300_30_week = cmp_dtw_sorted_list_cal(cal_list_cmp)
f_dtw_sorted = open('sorted_dtw_list_300_30', 'wb')
pickle.dump(sorted_dtw_list_split_300_30_week, f_dtw_sorted, True)
f_dtw_sorted.close()
sorted_edr_list_split_300_30_week = cmp_edr_sorted_list_cal(cal_list_cmp, 200)

f_edr_sorted = open('sorted_edr_list_300_30', 'wb')

pickle.dump(sorted_edr_list_split_300_30_week, f_edr_sorted, True)

f_edr_sorted.close()