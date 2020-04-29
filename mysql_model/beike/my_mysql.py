# -*- coding:utf-8 -*-
__author__ = "leo"

import pymysql

from mysql_model.model import House_Info


def save_house_info_to_mysql(info_list):
    try:
        db_connection = get_connection()
        cursor = db_connection.cursor()
        for info in info_list:
            for key, value in info.items():
                sql = "insert into house_info(price_part, price_info) values (\"{}\", \"{}\")".format(key, value)
                print(sql)
                cursor.execute(sql)
                db_connection.commit()

    finally:
        close_db(db_connection, cursor)


def get_connection():
    db_connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database='python_ui',
        charset="utf8"
    )
    return db_connection


def close_db(db_connection, cursor):
    cursor.close()
    db_connection.close()


def new_save_house_info_to_mysql(info_list):
    houses = House_Info()
    for info in info_list:
        for key, value in info.items():
            houses.insert(["price_part", "price_info"], [str(key), str(value)])
