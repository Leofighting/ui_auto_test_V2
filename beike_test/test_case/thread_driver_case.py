# -*- coding:utf-8 -*-
__author__ = "leo"

import time
from threading import Thread

from selenium.webdriver.common.by import By

from beike_test.config.basic_config import USERNAME, PASSWORD
from beike_test.pages.house_login_page import HouseLoginPage
from beike_test.pages.houses_info_page import HousesInfoPage
from beike_test.utils.browser_engine import browser_engine
from beike_test.config import logging_setting, basic_config
from beike_test.pages.houses_list_page import HousesListPage


class RemoteDriverCase(object):
    logger = logging_setting.get_logger()

    def save_info(self, system_name, url):
        driver = browser_engine.init_driver(url)
        city_name = ""
        self.logger.debug("开始保存房屋费用信息~~")
        self.logger.info("正在使用 {} 上的 Chrome 浏览器进行测试".format(system_name))
        # 登陆
        houses_login_page = HouseLoginPage(driver)
        houses_login_page.get_login_page(USERNAME, PASSWORD)
        # 获取筛选后的房屋列表
        houses_list_page = HousesListPage(driver)
        if system_name == "linux":
            city_name = "深圳"
        elif system_name == "windows":
            city_name = "广州"

        houses_list_page.get_houses_list_driver("exchange", city_name, "租房")
        self.logger.info("正在访问 {} 的租房信息".format(city_name))

        rent_type_locator = (By.LINK_TEXT, "合租")
        price_range_locator = (By.LINK_TEXT, "1000-1500元")
        newest_locator = (By.LINK_TEXT, "最新上架")
        houses_list_page.get_selector_page([rent_type_locator, price_range_locator, newest_locator])
        self.logger.debug("得到筛选后的页面~~")

        houses_locator = (By.XPATH, "//div[@class='content__list']//div[1]//a[1]//img[1]")
        driver = houses_list_page.get_houses_info_page(houses_locator)
        self.logger.info("当前房屋信息的 url 地址是：{}".format(driver.current_url))
        # 保存房屋费用信息到数据库中
        try:
            houses_info = HousesInfoPage(driver)
            houses_info.save_product_info()
            self.logger.info("保存商品信息成功~")
            return True
        except:
            return False
        finally:
            # 关闭浏览器
            time.sleep(3)
            driver.quit()


def thread_driver():
    address = basic_config.REMOTE_DRIVER_DICT
    threads = []
    for system_name, url in address.items():
        t = Thread(target=RemoteDriverCase().save_info, args=(system_name, url))
        threads.append(t)

    for t in threads:
        t.start()
