# -*- coding:utf-8 -*-
__author__ = "leo"

from mysql_model.field import Field
from mysql_model.my_database import create_pool


class ModelMetaClass(type):
    """定义元类，控制 model 对象的创建"""

    def __new__(cls, table_name, bases, attrs):
        if table_name == "Model":
            return super().__new__(cls, table_name, bases, attrs)

        mappings = dict()

        for k, v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs["__table__"] = table_name.lower()
        attrs["__mappings__"] = mappings
        return super().__new__(cls, table_name, bases, attrs)


class Model(dict, metaclass=ModelMetaClass):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def insert(self, column_list, param_list):
        print("执行 insert 方法")
        fields = []
        for k, v in self.__mappings__.items():
            fields.append(k)
        for key in column_list:
            if key not in fields:
                raise RuntimeError("此字段没有发现~~")
        # 检查参数的合法性
        args = self.__check_params(param_list)

        sql = "insert into {} ({}) values ({})".format(self.__table__, ",".join(column_list), ",".join(args))

        res = self.__do_execute(sql)
        print(res)

    def __check_params(self, param_list):
        args = []
        for param in param_list:
            if "\"" in param:
                param = param.replace("\"", "\\\"")
            param = "\"" + param + "\""
            args.append(param)

        return args

    def __do_execute(self, sql):
        conn = create_pool()
        cur = conn.cursor()
        print(sql)

        if "select" in sql:
            cur.execute(sql)
            result = cur.fetchall()
        else:
            result = cur.execute(sql)
        conn.commit()
        cur.close()
        return result

    def select(self, column_list, where_list):
        print("调用 select 方法")
        args = []
        fields = []

        for k, v in self.__mappings__.items():
            fields.append(k)

        for key in where_list:
            args.append(key)

        for key in column_list:
            if key not in fields:
                raise RuntimeError("此字段不存在~~")

        sql = "select {} from {} where {}".format(','.join(column_list), self.__table__, " and ".join(args))
        result = self.__do_execute(sql)
        return result

    def update(self, set_column_list, where_list):
        print("调用 update 方法")
        args = []
        fields = []

        for key in set_column_list:
            fields.append(key)

        for key in where_list:
            args.append(key)

        for key in set_column_list:
            if key not in fields:
                raise RuntimeError("此字段不存在~~")

        sql = "update {} set {} where {}".format(self.__table__, ",".join(set_column_list), " and ".join(args))
        result = self.__do_execute(sql)
        return result

    def delete(self, where_list):
        print("调用删除方法")
        args = []
        for key in where_list:
            args.append(key)

        sql = "delete from {} where {}".format(self.__table__, " and ".join(args))
        result = self.__do_execute(sql)

        return result
