# -*- coding:utf-8 -*-
__author__ = "leo"

from mysql_model.field import Field
from mysql_model.orm import Model


class House_Info(Model):
    price_part = Field("price_part", "varchar(255")
    price_info = Field("price_info", "text")


house = House_Info()
# house.insert(["price_part", "price_info"], ["月组价", "1000"])
house.update(["price_info='12000元'"], ["id=3"])
result = house.select(["price_part", "price_info"], ["id=3"])
print(result)
