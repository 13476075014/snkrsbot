#coding=utf-8
import requests,time,json
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
#无界面
#chromeOptions.add_argument('--headless')
#关闭图片
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
#禁用gpu加速
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
time.sleep(8)
acookies = browser.get_cookies()
cookie=""
if acookies != None:
    for i in acookies:
        cookie += (i['name'] + "=" + i['value'] + ";")
print cookie
x=requests.get("https://www.nike.com/cn/launch/?s=upcoming",cookies=cookie)
print x.content
#print(browser.page_source)
time.sleep(10)
#browser.close()
