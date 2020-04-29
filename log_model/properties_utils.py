# -*- coding:utf-8 -*-
__author__ = "leo"


class Properties:
    def __init__(self, file_name):
        self.properties_file_name = file_name
        self.properties = {}

    def get_properties(self):
        with open(self.properties_file_name, "r") as pro_file:
            for line in pro_file.readlines():
                line = line.strip().replace("\n", "")
                if line.find("#") != -1:
                    line = line[0: line.find("#")]

                if line.find("=") > 0:
                    line_list = line.split("=")
                    self.__get_dict(line_list[0].strip(), self.properties, line_list[1].strip())

        return self.properties

    def __get_dict(self, key_name, result_dict, value):
        if key_name.find(".") > 0:
            k = key_name.split(".")[0]
            result_dict.setdefault(k, {})
            return self.__get_dict(key_name[len(k) + 1:], result_dict[k], value)
        else:
            result_dict[key_name] = value
