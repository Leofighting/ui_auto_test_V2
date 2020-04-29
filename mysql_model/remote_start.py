# -*- coding:utf-8 -*-
__author__ = "leo"

from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from mysql_connect.beike import beike


def to_beike(name, server_address):
    print(name, " 启动")
    driver = webdriver.Remote(
        command_executor=server_address,
        desired_capabilities=DesiredCapabilities.CHROME
    )
    driver.maximize_window()

    if name == "linux":
        beike.shenzhen_start(driver)
    if name == "windows":
        beike.guangzhou_start(driver)


my_address = {
    "linux": "http://192.168.31.180:4444/wd/hub",
    "windows": "http://192.168.31.192:4444/wd/hub"
}

threads = []

for name, url in my_address.items():
    t = Thread(target=to_beike, args=(name, url))
    threads.append(t)

for t in threads:
    t.start()
