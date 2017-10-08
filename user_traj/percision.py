import pymysql
import pickle
import matplotlib.pyplot as plt

def cal_percision(rec_list,test_list):
    #取排名最高的5个好友，获取每个好友所有额推荐地点
    #test_list为测试集计算得到的兴趣点轨迹，此时不考虑轨迹，只考虑地点
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(rec_list)
def cal_recall(rec_list, test_list):
    insert_list = [rec_poi for rec_poi in rec_list if rec_poi in test_list]
    return len(insert_list), len(test_list)


def get_rec_list(sorted_list, set_size):
    db = pymysql.connect("localhost","root","Meituan-0502","user_trajectory")
    cursor = db.cursor()
    hit_t = 0
    rec_t = 0
    unhit_num = 0
    total_num = 0
    for sort_poi in sorted_list:
        for k, v in sort_poi.items():
            ori_poi_sql = """ SELECT REC_POI FROM rec_list_300_30 where DEVICEID='%s' """ % k
            cursor.execute(ori_poi_sql)
            ori_poi = cursor.fetchall()
            rec_users = [[users[0] for users in v[:set_size]]]
            # if not rec_users[0]:
            #     unhit_num += 1
            #     break
            rec_poi_sql = 'SELECT REC_POI FROM rec_list_300_30 where DEVICEID in %s '
            cursor.execute(rec_poi_sql, rec_users)
            rec_pois = cursor.fetchall()
            rec_poi = []
            for r in rec_pois:
                l_temp = r[0].split(',')
                rec_poi.extend(l_temp)
            hit_num, total_rec_num = cal_percision({}.fromkeys(rec_poi).keys(), list(ori_poi[0][0].split(',')))
            if hit_num == 0:
                unhit_num += 1
            hit_t += hit_num
            rec_t += total_rec_num
            total_num += 1
    print("推荐未命中兴趣点数量为： %d" % unhit_num)
    print("推荐总数量为： %d" % total_num)
    print("推荐兴趣点总数量为： %d" % rec_t)
    print("推荐命中兴趣点总数量为： %d" % hit_t)
    return (total_num-unhit_num)/total_num


def insert_rec_db(cal_list):
    db = pymysql.connect("localhost","root","Meituan-0502","user_trajectory")
    cursor = db.cursor()
    insert_list = []
    sql = 'INSERT INTO rec_list (DEVICEID, REC_POI) VALUES(%s,%s)'
    len_size = 0
    for cal_poi in cal_list:
        rec_poi_list = [tradj.get('typecode') for tradj in cal_poi.get('tradj')]
        rec_poi_str = ','.join(rec_poi_list)
        if len(rec_poi_str) > len_size:
            len_size = len(rec_poi_str)
        data = (cal_poi.get('deviceId'), rec_poi_str)
        insert_list.append(data)
    print(len_size)
    cursor.executemany(sql, insert_list)
    db.commit()
    db.close()

def get_split_rec_list(sorted_split_list, top_index=1):
    total_num = len(sorted_split_list)
    perfect_pre = 0
    success_pre = 0
    bad_pre = 0
    for sort_split_poi in sorted_split_list:
        for k, v in sort_split_poi.items():
            if k[29:] == "first":
                if (k.replace("first", "second"), v[0][1]) in [val[0] for val in v]:
                    perfect_pre += 1
                    success_pre += 1
                else:
                    try:
                        i = [val[0] for val in v].index()
                        if i <= top_index:
                            success_pre += 1
                    except:
                        bad_pre += 1
                        print("Bad precision")
            else:
                if (k.replace("second", "first"), v[0][1]) in [val[0] for val in v]:
                    perfect_pre += 1
                    success_pre += 1
                else:
                    try:
                        i = [val[0] for val in v].index()
                        if i <= top_index:
                            success_pre += 1
                    except:
                        bad_pre += 1
                        print("Bad precision")

    success_rate = success_pre/total_num
    perfect_rate = perfect_pre/total_num

    print(success_rate)
    print(perfect_rate)



# f_cal = open('cal_list_split_300_30', 'rb')
# cal_list = pickle.load(f_cal)
# f_cal.close()
# insert_rec_db(cal_list)
# f_sorted = open('sorted_list_split_300_30', 'rb')
# sorted_split_list = pickle.load(f_sorted)
# f_sorted.close()
# get_split_rec_list(sorted_split_list, 10)

# print(cal_list)
# print(sorted_list)

# f_sorted = open('sorted_list_300_30', 'rb')
# sorted_list = pickle.load(f_sorted)
# print(sorted_list)
# prec_1 = get_rec_list(sorted_list, 5)
# f_cmp_sorted = open("sorted_edr_list_300_30", 'rb')
# cmp_sorted_list = pickle.load(f_cmp_sorted)
group_labels = [i for i in range(3, 21)]
x1 = group_labels
x2 = x1
x3 = x2
x4 = x3
# y1 = []
# y2 = []
# y3 = []
# y4 = []
#
# f_sorted = open('sorted_list_300_30_week', 'rb')
# sorted_list_1 = pickle.load(f_sorted)
# f_sorted.close()
#
# f_sorted_2 = open('sorted_list_300_30', 'rb')
# sorted_list_2 = pickle.load(f_sorted_2)
# f_sorted_2.close()
#
# f_sorted_3 = open('sorted_dtw_list_300_30', 'rb')
# sorted_list_3 = pickle.load(f_sorted_3)
# f_sorted.close()
#
# f_sorted_4 = open('sorted_edr_list_300_30', 'rb')
# sorted_list_4 = pickle.load(f_sorted_4)
# f_sorted.close()
# for i in group_labels:
    # prec_1 = get_rec_list(sorted_list_1, i)
    # y1.append(prec_1)
    # prec_2 = get_rec_list(sorted_list_2, i)
    # y2.append(prec_2)
    # prec_3 = get_rec_list(sorted_list_3, i)
#     y3.append(prec_3)
#     prec_4 = get_rec_list(sorted_list_4, i)
#     y4.append(prec_4)
#
# print(y2)
y1 = [0.8940397350993378, 0.9072847682119205, 0.9304635761589404, 0.9337748344370861, 0.9437086092715232, 0.9437086092715232, 0.9470198675496688, 0.9503311258278145, 0.956953642384106, 0.9602649006622517, 0.9635761589403974, 0.9635761589403974, 0.9635761589403974, 0.9668874172185431, 0.9701986754966887, 0.9701986754966887, 0.9735099337748344, 0.9735099337748344]
y2 = [0.804635761589404, 0.8410596026490066, 0.8708609271523179, 0.8841059602649006, 0.8973509933774835, 0.9006622516556292, 0.9072847682119205, 0.9072847682119205, 0.9139072847682119, 0.9172185430463576, 0.9205298013245033, 0.9238410596026491, 0.9271523178807947, 0.9337748344370861, 0.9370860927152318, 0.9370860927152318, 0.9403973509933775, 0.9403973509933775]
y3 = [0.5960264900662252, 0.6456953642384106, 0.6821192052980133, 0.7218543046357616, 0.7450331125827815, 0.7483443708609272, 0.7615894039735099, 0.7649006622516556, 0.7781456953642384, 0.7947019867549668, 0.8245033112582781, 0.8377483443708609, 0.8443708609271523, 0.8576158940397351, 0.8642384105960265, 0.8741721854304636, 0.8807947019867549, 0.8807947019867549]
y4 = [0.5662251655629139, 0.6423841059602649, 0.7119205298013245, 0.7781456953642384, 0.7947019867549668, 0.8211920529801324, 0.8344370860927153, 0.8443708609271523, 0.8675496688741722, 0.8741721854304636, 0.8807947019867549, 0.8841059602649006, 0.890728476821192, 0.8940397350993378, 0.8973509933774835, 0.9072847682119205, 0.9105960264900662, 0.9139072847682119]

plt.title("recommend set size vs precision")

plt.xlabel("recommend set size")

plt.ylabel("precision %")

plt.plot(x1, y1, 'r', label='RI-STS-W')
plt.plot(x2, y2, 'b', label='RI-STS')
plt.plot(x3, y3, 'y', label='EDR')
plt.plot(x4, y4, 'g', label='DTW')
plt.xticks(x3, group_labels, rotation=0)

plt.legend(bbox_to_anchor=[0.3, 0.8])
plt.grid()
plt.show()
#
# print(group_labels)