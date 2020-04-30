# -*- coding:utf-8 -*-
__author__ = "leo"

from selenium .webdriver.common.by import By

from beike_test.pages.houses_info_page import HousesInfoPage
from beike_test.utils.browser_engine import browser_engine
from beike_test.config import logging_setting
from beike_test.pages.houses_list_page import HousesListPage


class Test(object):
    driver = browser_engine.init_local_driver()
    logger = logging_setting.get_logger()

    def test_save_info(self):
        self.logger.debug("开始保存房屋费用信息~~")
        houses_list_page = HousesListPage(self.driver)
        houses_list_page.get_houses_list_driver("exchange", "深圳", "租房")

        rent_type_locator = (By.LINK_TEXT, "合租")
        price_range_locator = (By.LINK_TEXT, "1000-1500元")
        newest_locator = (By.LINK_TEXT, "最新上架")
        houses_list_page.get_selector_page([rent_type_locator, price_range_locator, newest_locator])
        self.logger.debug("得到筛选后的页面~~")

        houses_locator = (By.XPATH, "//div[@class='content__list']//div[1]//a[1]//img[1]")
        driver = houses_list_page.get_houses_info_page(houses_locator)
        self.logger.info("当前房屋信息的 url 地址是：{}".format(driver.current_url))

        houses_info = HousesInfoPage(driver)
        houses_info.save_product_info()
        self.logger.info("保存商品信息成功~")


t = Test()
t.test_save_info()