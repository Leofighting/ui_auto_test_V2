# -*- coding:utf-8 -*-
__author__ = "leo"

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import json

driver = webdriver.Chrome()
driver.maximize_window()


def login():
    """登陆"""
    driver.get("https://ke.com")
    driver.find_element_by_class_name("btn-login").click()
    driver.find_element_by_link_text("账号密码登录").click()
    driver.find_element_by_class_name("phonenum_input").send_keys("18819151992")
    driver.find_element_by_class_name("password_input").send_keys("1234QWER")
    driver.find_element_by_class_name("login_submit").click()
    # 保存 cookies 到文件中
    save_cookies_to_file(driver)


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


def check_cookies():
    """检查 cookies 是否存在"""
    # 设置登陆状态，初始值为 False
    login_status = False
    # 将 cookies 信息保存到driver中
    driver = save_cookies_to_driver()

    # 进行跳转连接校验
    driver.get("https://user.ke.com/site/favorHouse/")
    current_url = driver.current_url

    if current_url == "https://user.ke.com/site/favorHouse/":
        login_status = True
        return login_status
    else:
        return login_status


def save_cookies_to_driver():
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


def to_rend_page():
    """跳转到 深圳 具体的租房信息页面"""
    driver.get("https://ke.com")
    location = driver.find_element_by_class_name("exchange")
    ActionChains(driver).move_to_element(location).perform()
    time.sleep(1)
    location.click()

    driver.find_element_by_link_text("深圳").click()
    driver.find_element_by_link_text("租房").click()
    driver.find_element_by_link_text("南山区").click()
    driver.find_element_by_link_text("合租").click()
    driver.find_element_by_link_text("最新上架").click()
    driver.find_element_by_xpath("//div[@class='content__list']//div[1]//a[1]//img[1]").click()

    # 切换句柄
    house_handle = driver.current_url
    handles = driver.window_handles

    for handle in handles:
        if handle != house_handle:
            driver.switch_to.window(handle)

    # 使用 js语句 往下滚动页面
    js = "window.scrollTo(0, 100)"
    driver.execute_script(js)
    # 点击 费用详情
    driver.find_element_by_xpath("/html[1]/body[1]/div[3]/div[1]/div[3]/div[3]/ul[1]/li[3]").click()
    # 解析所有的标签
    info_elements = driver.find_elements_by_class_name("cost_content")
    print(info_elements, len(info_elements))
    # 定义一个 list 存储最终结果
    result_list = []
    # 逐个解析标签
    for info_element in info_elements:
        info_element_dict = get_info_element_dict(info_element)
        result_list.append(info_element_dict)
    # 保存信息到文件中
    save_house_info(result_list)


def get_info_element_dict(info_element):
    """获取元素信息"""
    price_part = info_element.find_element_by_class_name("title_info")
    # 获取表格标题信息
    table_title = info_element.find_element_by_class_name("table_title")
    table_title_key = table_title.find_elements_by_tag_name("li")
    # 获取表格内容信息
    table_content = info_element.find_element_by_class_name("table_content")
    table_content_value = table_content.find_elements_by_tag_name("li")

    # 存储每种费用信息的 key 与 value
    key_and_value_dict = {}
    # 存储所有费用详情的信息
    parts_dict = {}

    for i in range(len(table_title_key)):
        table_title_key_str = table_title_key[i].text.split("<span")[0]
        table_content_value_str = table_content_value[i].text
        key_and_value_dict[table_title_key_str] = table_content_value_str

    parts_dict[price_part.text] = key_and_value_dict

    return parts_dict


def save_house_info(info_list):
    """保存 房屋信息 到文件中"""
    project_path = os.getcwd()
    file_path = project_path + "/house_infos/"
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    with open(file_path + "house.infos", "a", encoding="utf-8") as f:
        f.write(str(info_list))
        print(str(info_list))


if __name__ == '__main__':
    # 判断登陆是否成功
    try:
        loop_status = True
        # 检验 cookies 是否生效
        while loop_status:
            login_status = check_cookies()

            if login_status:
                loop_status = False
            else:
                login()
                loop_status = False
        # 跳转到 深圳 租房信息页面
        to_rend_page()

    finally:
        time.sleep(2)
        driver.quit()
