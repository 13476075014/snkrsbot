#coding=utf-8
import requests,time
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument('--disable-gpu')
browser=webdriver.Chrome(chrome_options=chromeOptions)
browser.get("https://www.nike.com/cn/zh_cn/")
login=browser.find_element_by_class_name("login-text")
login.click()
login1=browser.find_elements_by_tag_name("a")
login1[264].click()
username=browser.find_element_by_name("emailAddress")
username.send_keys("lktop@vip.qq.com")
password=browser.find_element_by_name("password")
password.send_keys("huanxiangmf1Q")
loginbu=browser.find_elements_by_tag_name("input")
loginbu[7].click()
#print(browser.page_source)
time.sleep(10)
#browser.close()
