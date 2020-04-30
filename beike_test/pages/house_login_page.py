# -*- coding:utf-8 -*-
__author__ = "leo"

from selenium.webdriver.common.by import By

from beike_test.config import basic_config
from beike_test.config.logging_setting import get_logger
from beike_test.pages.base_page import BasePage


class HouseLoginPage(BasePage):
    logger = get_logger()

    def __init__(self, driver):
        self._driver = driver
        super().__init__(driver, basic_config.START_URL)

    def login(self, username, password):
        driver = self.open()
        login_button_element = (By.CLASS_NAME, "reg")
        change_type_element = (By.CLASS_NAME, "change_login_type _color")
        username_element = (By.CLASS_NAME, "phonenum_input")
        password_element = (By.CLASS_NAME, "password_type password_input")
        submit_element = (By.CLASS_NAME, "confirm_btn ")

        login_button = self.find_element(*login_button_element)
        login_button.click()
        change_type = self.find_element(*change_type_element)
        change_type.click()
        username_ele = self.find_element(*username_element)
        username_ele.send_keys(username)
        password_ele = self.find_element(*password_element)
        password_ele.send_keys(password)
        submit = self.find_element(*submit_element)
        submit.click()

        # 切换句柄
        handles = driver.window_handles
        index_handle = driver.current_window_handle
        for handle in handles:
            if handle != index_handle:
                driver.close()
                driver.switch_to.window(handle)

        self._driver = driver
        return driver
