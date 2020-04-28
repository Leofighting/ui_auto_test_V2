# -*- coding:utf-8 -*-
__author__ = "leo"

import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from threading import Thread


def to_baidu(name, server_address):
    print(name)
    driver = webdriver.Remote(
        command_executor=server_address,
        desired_capabilities=DesiredCapabilities.CHROME
    )

    driver.get("https://www.baidu.com")
    time.sleep(3)
    driver.quit()


address = {
    "linux": "http://192.168.31.180:4444/wd/hub",
    "windows": "http://192.168.31.192:4444/wd/hub"
}


threads = []

for name, url in address.items():
    t = Thread(target=to_baidu, args=(name, url))
    threads.append(t)

for t in threads:
    t.start()