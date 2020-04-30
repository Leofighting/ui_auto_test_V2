# -*- coding:utf-8 -*-
__author__ = "leo"

from beike_test.orm.field import Field
from beike_test.orm.orm import Model


class House_Info(Model):
    price_part = Field("price_part", "varchar(255")
    price_info = Field("price_info", "text")