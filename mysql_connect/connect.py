# -*- coding:utf-8 -*-
__author__ = "leo"

import pymysql

db_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database='python_ui',
    charset="utf8"
)

cursor = db_connection.cursor()
sql = "insert into house_info(price_part, price_info) values('年租价', '10000元')"
cursor.execute(sql)
db_connection.commit()
cursor.close()
db_connection.close()
