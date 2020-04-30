# -*- coding:utf-8 -*-
__author__ = "leo"

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from beike_test.config import basic_config


class BrowserEngine:

    @staticmethod
    def init_local_driver():
        """
        初始化本地 driver
        :return: 返回一个 Chrome driver
        """
        option = webdriver.ChromeOptions()
        option.add_argument("disable-infobars")
        driver = webdriver.Chrome(chrome_options=option)

        return driver

    @staticmethod
    def init_remote_driver():
        """
        初始化远程 driver，详细配置见 basic_config.py
        :return: result_dict 字典类型，具体结构：{"名字": driver}
        """
        remote_browser_dict = basic_config.REMOTE_DRIVER_DICT
        # 储存返回结果
        result_dict = {}

        for name, url in remote_browser_dict.items():
            option = webdriver.ChromeOptions()
            option.add_argument("disable-infobars")
            driver = webdriver.Remote(
                command_executor=url,
                desired_capabilities=DesiredCapabilities.CHROME
            )
            result_dict[name] = driver

        return result_dict

    @staticmethod
    def init_local_driver_no_gui():
        """
        无界面运行本地 driver
        :return: 返回一个 Chrome driver
        """
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")  # 修改参数
        driver = webdriver.Chrome(chrome_options=option)

        return driver


browser_engine = BrowserEngine()