import _pickle as pickle
import datetime

app_key_list = ["52c469b8f1f26f14c28576d2d4b6e87c",
                "ffc6fead741c315a8cc4876e07bab825",
                "5cee07ef7640065cb182e870da66c7e1",
                "e908e95d55dba5c8ec0089ddf5dc26e9",
                "aa6783184da566114a4365c76e6a90ec",
                "7ee9abe8c41894e05a825016661d5910",
                "8c7f2f9d4607e4de174bf7e703f86de2",
                "36a95e53e2977825875b968ad1f73238",
                "5c95eeb4c28e0e0bfefd182eda0b2b35",
                "51444c5064e6501a308290f433feff30", ]

# f = open('pickle_file', 'wb')

# c = pickle.dump(app_key_list, f, True)

# f.close()
# f1 = open('cal_list_200', 'rb')
#
# f2 = open('cal_list_250', 'rb')

# list_11 = [("t3",3),("t1",1),("t2",2)]

# list_11.sort(key=lambda tup: tup[1])

# print(list_11)

f3 = open('sorted_list', 'rb')

# c1 = pickle.load(f1)
# c2 = pickle.load(f2)
c3 = pickle.load(f3)

print(c3)

f3.close()
# print(len(c1))
# print(len(c2))

# print(len(c3))

# print(c2 == c3)
# f2.close()
#
# print(c3)
# s = {'deviceId': '351671070295053_14b37001f63b', 'tradj': [{'timestamp': datetime.datetime(2016, 9, 25, 16, 54, 34), 'typecode': '050100'}]}
# str_s = str(s)