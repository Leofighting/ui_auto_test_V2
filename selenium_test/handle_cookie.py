# -*- coding:utf-8 -*-
__author__ = "leo"


from selenium import webdriver
import time
import os
import json

driver = webdriver.Chrome()
driver.maximize_window()


def save_cookies(driver):
    """保存cookies 到文件中"""
    project_path = os.getcwd()
    file_path = project_path + "/cookies/"

    if not os.path.exists(file_path):
        os.mkdir(file_path)

    # 从 driver 当中获取到 cookies
    cookies = driver.get_cookies()
    # 保存 cookies 信息到文件中
    file = file_path + "beike.cookies"
    with open(file, "w") as f:
        # 使用 json.dump 写入
        json.dump(cookies, f)


def get_url_with_cookies():
    """
    携带cookies访问页面
    使用个人中心页面验证cookies是否有效
    """
    # 获取cookies文件
    project_path = os.getcwd()
    file_path = project_path + "/cookies/"
    file = file_path + "beike.cookies"

    bk_cookies_file = open(file, "r")
    bk_cookies_str = bk_cookies_file.readline()

    # 加载 cookies 信息
    bk_cookies_dict = json.loads(bk_cookies_str)
    print(bk_cookies_dict)
    time.sleep(5)
    # 先访问网站，删除旧的 cookies ，再添加读取到的 cookies
    driver.get("https://fs.ke.com")
    driver.delete_all_cookies()
    for cookie in bk_cookies_dict:
        if "expiry" in cookie:
            del cookie["expiry"]
        driver.add_cookie(cookie)
    time.sleep(5)
    # 验证 cookies 是否有效
    driver.get("https://user.ke.com/site/favorHouse/")
    time.sleep(5)
    driver.quit()



def login():
    """登陆"""
    try:
        driver.get("https://fs.ke.com")
        driver.find_element_by_class_name("btn-login").click()
        driver.find_element_by_link_text("账号密码登录").click()
        driver.find_element_by_class_name("phonenum_input").send_keys("18819151992")
        driver.find_element_by_class_name("password_input").send_keys("1234QWER")
        driver.find_element_by_class_name("login_submit").click()
        # 保存 cookies 到文件中
        save_cookies(driver)
    finally:
        time.sleep(3)
        driver.quit()


if __name__ == '__main__':
    # login()
    get_url_with_cookies()