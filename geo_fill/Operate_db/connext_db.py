import pymysql

db = pymysql.connect("localhost","root","123456","user_trajectory")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS beijing")
sql = """CREATE TABLE beijing (
        ID INT auto_increment primary key,
        TIMESTAMP DATETIME,
        DEVICEID CHAR(200) NOT NULL,
        LONGITUDE DECIMAL(9,6),
        LATITUDE  DECIMAL(9,6)
)"""

cursor.execute(sql)

db.close()