# -*- coding:utf-8 -*-
__author__ = "leo"

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json


def save_cookies_to_file(driver):
    """把 cookies 保存到文件中"""
    # 获取文件路径
    file_path = get_cookies_dir()
    # 获取 cookies
    cookies = driver.get_cookies()
    # 存储cookies 到文件中
    with open(file_path + "bk.cookies", "w") as f:
        json.dump(cookies, f)


def get_cookies_dir():
    """获取 cookies 保存路径"""
    project_path = os.getcwd()
    file_path = project_path + "/cookies/"

    if not os.path.exists(file_path):
        os.mkdir(file_path)
    return file_path


def check_cookies(driver):
    """检查 cookies 是否存在"""
    # 设置登陆状态，初始值为 False
    login_status = False
    # 将 cookies 信息保存到driver中
    driver = save_cookies_to_driver(driver)

    # 进行跳转连接校验
    driver.get("https://user.ke.com/site/favorHouse/")
    current_url = driver.current_url

    if current_url == "https://user.ke.com/site/favorHouse/":
        login_status = True
        return login_status
    else:
        return login_status


def save_cookies_to_driver(driver):
    cookies_file = get_cookies_file()
    with open(cookies_file, "r") as f:
        bk_cookies_str = f.readline()
        bk_cookies_dict = json.loads(bk_cookies_str)

    # 清除旧的 cookies 信息
    driver.get("https://ke.com")
    driver.delete_all_cookies()

    for cookie in bk_cookies_dict:
        if "expiry" in cookie:
            del cookie["expiry"]
        driver.add_cookie(cookie)

    return driver


def get_cookies_file():
    """获取 cookies 文件"""
    return get_cookies_dir() + "bk.cookies"
