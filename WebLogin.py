#coding=utf-8
import json
import random
import traceback
import requests,time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait


class WebLogin_Chrome:
    def __init__(self, username, password):
        self.cookies = None
        self.session = requests.session()
        self.userInfo = None
        self.username = username
        self.password = password

    def login(self):
        chromeOptions = webdriver.ChromeOptions()
        # 无界面
        # chromeOptions.add_argument('--headless')
        # 关闭图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        # 禁用gpu加速
        chromeOptions.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chromeOptions)

        browser.get("https://www.nike.com/cn/zh_cn/")
        login = browser.find_element_by_class_name("login-text")
        login.click()
        login1 = browser.find_elements_by_tag_name("a")
        login1[264].click()
        username = browser.find_element_by_name("emailAddress")
        username.send_keys("lktop@vip.qq.com")
        password = browser.find_element_by_name("password")
        password.send_keys("huanxiangmf1Q")
        loginbu = browser.find_elements_by_tag_name("input")
        loginbu[7].click()
        time.sleep(5)
        self.cookies = browser.get_cookies()

    def getCookies(self):
        cookies = ""
        if self.cookies != None:
            for cookie in self.cookies:
                cookies += (cookie['name'] + "=" + cookie['value'] + ";")
        return cookies