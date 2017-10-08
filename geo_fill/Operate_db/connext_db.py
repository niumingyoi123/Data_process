import pymysql

db = pymysql.connect("localhost","root","123456","user_trajectory")
cursor = db.cursor()

bssids = [["351671070295053_14b37001f63b", "351824074135078_9C2A831EF337"]]



sql = """ SELECT * FROM `rec_list` WHERE `DEVICEID` in %s """

cursor.execute(sql, bssids)

result = cursor.fetchall()
print(result)
db.close()