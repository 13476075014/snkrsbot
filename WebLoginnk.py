#coding=utf-8
import json
import random
import traceback
import requests
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
        try:
            chromeOptions = webdriver.ChromeOptions()
            # 无界面
            # chromeOptions.add_argument('--headless')
            # 禁用gpu加速
            chromeOptions.add_argument('--disable-gpu')
            # 关闭图片
            prefs = {"profile.managed_default_content_settings.images": 2}
            chromeOptions.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(chrome_options=chromeOptions)

            w_h = driver.get_window_size()
            width = w_h["width"]
            height = w_h["height"]

            clickWidth1 = (width - 500) / 2
            clickWidth2 = width / 2 + 250

            driver.get("https://www.nike.com/cn/zh_cn/")
            WebDriverWait(driver, 15).until(lambda x: x.find_element_by_class_name('login-text'))
            driver.find_element_by_class_name('login-text').click()

            # 随机位置点击绕过验证
            for i in range(random.randint(2, 5)):
                ActionChains(driver).move_by_offset(clickWidth1,
                                                    random.randint(0, height)).click().perform()
                ActionChains(driver).move_by_offset(clickWidth2,
                                                    random.randint(0, height)).click().perform()

            driver.find_element_by_name('verifyMobileNumber').send_keys(self.username)
            driver.find_element_by_name('password').send_keys(self.password)
            driver.find_element_by_class_name('nike-unite-submit-button').click()

            # 随机位置点击绕过验证
            for i in range(random.randint(2, 5)):
                ActionChains(driver).move_by_offset(clickWidth1,
                                                    random.randint(0, height)).click().perform()
                ActionChains(driver).move_by_offset(clickWidth2,
                                                    random.randint(0, height)).click().perform()
            try:
                WebDriverWait(driver, 5).until_not(
                    lambda x: x.find_element_by_class_name('exp-join-login').is_displayed())
            except:
                # print("等待超时...")
                pass
            if not driver.find_element_by_xpath('//*[@id="nike-unite-mobileLoginForm"]/div[1]').is_displayed():
                WebDriverWait(driver, 10).until_not(
                    lambda x: x.find_element_by_class_name('exp-join-login').is_displayed())

                self.cookies = driver.get_cookies()

                driver.get("https://unite.nike.com/session.html")
                userInfo = driver.execute_script(
                    "return localStorage.getItem('com.nike.commerce.nikedotcom.web.credential');")
                self.userInfo = json.loads(userInfo)
        except:
            traceback.print_exc()
        finally:
            driver.close()
            driver.quit()

    def getCookies(self):
        cookies = ""
        if self.cookies != None:
            for cookie in self.cookies:
                cookies += (cookie['name'] + "=" + cookie['value'] + ";")
        return cookies