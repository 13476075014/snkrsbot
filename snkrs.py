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
time.sleep(5)
acookies = browser.get_cookies()
cookie=""
if acookies != None:
    for i in acookies:
        cookie += (i['name'] + "=" + i['value'] + ";")
#print cookie
head={
"accept":"*/*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"cache-control": "no-cache",
"cookie": '''AnalysisUserId=183.60.197.103.103401539491276992; anonymousId=7BE12371D7FF8715B6B0BD9D408C75CE; guidU=a6e97f21-5101-459e-adf7-e585e219da0d; neo.swimlane=45; cicPWIntercept=1; _gcl_au=1.1.1525637876.1539491304; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%227BE12371D7FF8715B6B0BD9D408C75CE%22; CONSUMERCHOICE_SESSION=t; RES_TRACKINGID=777245231343142; ResonanceSegment=1; _gscu_207448657=394913175rv8lz17; _smt_uid=5bc2c5f5.4e697c8b; lls=3; siteCatalyst_sample=79; dreamcatcher_sample=19; neo_sample=53; NIKE_CART=b:c; NIKE_COMMERCE_COUNTRY=CN; NIKE_COMMERCE_LANG_LOCALE=zh_CN; CONSUMERCHOICE=cn/zh_cn; cicIntercept=1; neo.experiments=%7B%22main%22%3A%7B%223333-interceptor-cn%22%3A%22a%22%2C%220001%22%3A%22a%22%7D%2C%22thirdparty%22%3A%7B%7D%2C%22snkrs%22%3A%7B%7D%2C%22ocp%22%3A%7B%7D%7D; dreams_sample=81; DAPROPS="sdevicePixelRatio:1|sdeviceAspectRatio:16/9|bcookieSupport:1"; Hm_lvt_ed406c6497cc3917d06fd572612b4bba=1541683422; _qzja=1.1540173633.1541683422347.1541683422347.1541683422347.1541683432979.1541683432989..0.0.5.1; _abck=B8713214F31DF576A68BE3559AA55356~0~YAAQZCCEtv3oRNRmAQAA12Z+8wA1hKH/hKkH/aWS5uiD9vQK7fTMBGtJolG9lWI2X/zmxA5eCMXJRHvtWU5nJCtIImlL+fI3e6M+mQOQ4tY/Un7VOL/bhNiKzu5GKPrEASi3mOXVN4KklzIHu96JWy8mWB2uC8pAaBmWHD+3ByQV0eVV6ytzPLpWUXpyJYenk/jZzTbSmhVRYLxTJk3CAzQ2bxRl9C32zVChw4dVr7Cun6UWrFNAapvi4a8/haYUAKGyLGBsE8mHMooCsqa5NZEpPQ+WwGtRBcNjxLdOgshDryU55ZOn~-1~-1~-1; guidS=2e3cc0e5-50d7-48eb-d25d-e9c6c470fb60; guidSTimestamp=1541738243660|1541738447570; slCheck=p3R8AIZyGAY7sAexQaSJunIzfRoO6K5Ikpxtb/VQzdf3hLCKiK5PcS2ry12OQUL5LemYkFAUOM+ji1VpQLgNM7hIvEq6OMyEjH5v1u+wcaBKdV3S1ix0bDwu4Rj4KQxi; llCheck=ldrPb4mb57cawquFbnCVqtixTR/Wg/sHvJquFPTX6FAOVQUzkoEcExAJ3ZckFnLiUFFDAyUp0UQMGdUm6Avrupr0srhhYy9fYfpsRFccGhV+gBug5rUbYnyY1Yysz9/t/LAvxcNylGXQbo+RKPMg9OBDxsTITFcCc5d9kdBw8Ww=; bm_sz=92BB9CA0B2E244F7604A25B55720F54E~QAAQxPLzPy3rzdJmAQAAZOSN+A+OJESmuKu62THFSHWbZBTYTWSRNERhJwuhSvWExBXB9xCiXDSoRr8tYQlZzzZpJVDW8OBcrgrWl6CeV3M4Vo+XiHzD6Czbdsku41wFDDolvLTytI/UV2MEAwkI7n/AwtwPxdhUrFOHVrlJi8Oc9NFG1f+j9uCGgpPk; ak_bmsc=B30A0C36228384015D971BA8262590CDB73CC567865500008685E55BFF6D4E65~pl4mrzyOo/LOsTaYhqWemib8HzeuwcplVP2DgjLArOUdbyr9FdHjUEoO5F14OKMkrrjgNgjvX7/3tyEFWRHypxF3AYFNXQe83KuzSeasvdHQcmKNPakWQaxUDZtOj443ilwUnCxk2FQijIop8Y5+cf3ZdgBZjOrvBg+8AhAVp0DDxUTsWcXk+W82d0rYLjsXgVz4MOfUjMnNIdCb4nFxkHt7KALAbZwze13up4ih0RtteGDRTt0YomPvUjxYw3yZ+J3XMIoMsstlxdgzExpDlXvEAwZLUVgDrkP0wC4FLLH7hZmFWi7piphD0KS9BIWqBNPdwcN22P8jJ9kIIelqKWSQ==; mm_wc_pmt=1; _gscbrs_207448657=1; AMCVS_F0935E09512D2C270A490D4D%40AdobeOrg=1; AMCV_F0935E09512D2C270A490D4D%40AdobeOrg=690614123%7CMCIDTS%7C17845%7CMCMID%7C81273656479516255450967188602063724350%7CMCAAMLH-1542373508%7C11%7CMCAAMB-1542373508%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1541775908s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.0; APID=C7DF1D25802F715CFC07EA0268F217F9.sin-333-app-ap-0; sls=1; CART_SUMMARY=%7B%22profileId%22+%3A%2218571452869%22%2C%22userType%22+%3A%22DEFAULT_USER%22%2C%22securityStatus%22+%3A%221%22%2C%22cartCount%22+%3A0%7D; exp.swoosh.user=%7B%22granted%22%3A0%7D; RES_SESSIONID=173321429392054; ppd=homepage%7Cnikecom%3Ehomepage; utag_main=_st:1541770728072$ses_id:1541769412741%3Bexp-session; NIKE_CART_SESSION={%22bucket%22:%22jcart%22%2C%22country%22:%22CN%22%2C%22id%22:0%2C%22merged%22:false}; _gscs_207448657=41768707r37jpz19|pv:3; s_sess=%20c51%3Dhorizontal%3B%20prevList2%3D%3B%20s_cc%3Dtrue%3B%20tp%3D6122%3B%20s_ppv%3Dunified%252520profile%25253Elogin%252C15%252C15%252C947%3B; RT="sl=3&ss=1541768585969&tt=46230&obo=0&sh=1541768938553%3D3%3A0%3A46230%2C1541768922014%3D2%3A0%3A30002%2C1541768707214%3D1%3A0%3A4895&dm=nike.com&si=c7430edb-3a32-4e45-9f0f-da5df251b30a&bcn=%2F%2F17d98a5e.akstat.io%2F&ld=1541768938554&nu=https%3A%2F%2Fwww.nike.com%2Fcn%2Fzh_ch%2Fc%2Fnike-plus&cl=1541769101970&r=https%3A%2F%2Fwww.nike.com%2Fcn%2Fzh_cn%2F&ul=1541769101982&hd=1541769129944"; nike_locale=cn/zh_cn; bm_sv=86BA91B8A14E3ED6A91A03AB2314EED9~g5KC366LXL4lHnJyGJ8KXHvJ5zRyuIj1b2NsXu3JKAJJCvHCsaYhfxxeNAZrLjXZdqRF2MI6BZT1uD0ClpMQED9Swxl9ruus63OJfIqIqYXkz8dIpGNbfR9WJu1vJUSUpH86kAoD9mdxwdvIY1oDnMRNn8Pt3SSa6boOxsk76gc=; s_pers=%20c58%3Dno%2520value%7C1541770900873%3B%20s_dfa%3Dnikecomprod%7C1541770973836%3B''',
"pragma": "no-cache",
"referer": "https://www.nike.com/cn/zh_cn/e/nike-plus-membership",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}
x=requests.get("https://www.nike.com/cn/zh_cn/e/nike-plus-membership",headers=head)
print x.content
#print(browser.page_source)
time.sleep(10)
#browser.close()
