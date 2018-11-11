#coding=utf-8
from login import *
import json
import re
import requests
from WebLogin import *
import threading,sqlite3,time
from multiprocessing import Process,Queue


def getPostpayLink(productId, shoesLink):
    url = "https://api.nike.com/merch/products/v2/" + productId
    response = requests.get(url).json()
    postpayLink = shoesLink + "?LEStyleColor={styleColor}&LEPaymentType=Alipay".format(
        styleColor=response["styleColor"])
    return postpayLink


def buySet(shoesUrl):
    response = requests.get(shoesUrl).text

    launchId = re.findall(r"\"launchViewId\":\"(.*?)\"", response, re.S | re.I)[0]
    size = re.findall(r"\"sizes\":(.*?),\"_fetchedAt\"", response, re.S | re.I)[0]
    productId = re.findall(r"product\":{\"productId\":\"(.*?)\"", response, re.S | re.I)[0]

    shoesLink = re.findall(r"canonical\" href=\"(.*?)\"", response, re.S | re.I)[0]
    postpayLink = getPostpayLink(productId, shoesLink)

    stock = []
    outOfStock = []

    j_size = json.loads(size)

    for s in j_size:
        if j_size[s]["available"]:
            stock.append(j_size[s]["localizedSize"])
        else:
            outOfStock.append(j_size[s]["localizedSize"])
    stock.sort()
    outOfStock.sort()

    if len(outOfStock) > 0:
        print(" ".join(outOfStock) + "尺码缺货\n请选择" + " ".join(stock))
    else:
        print("所有尺码有货\n请选择" + " ".join(stock))

    shoesSize = input("-->")

    for s in j_size:
        if j_size[s]["localizedSize"] == shoesSize:
            usShoesSize = s
            skuId = j_size[s]["skuId"]

    # print("请设置好默认收货地址")

    # print("请选择支付方式 1.银联 2.微信 3.支付宝")
    # purMethod = input("-->")

    # shoesBuyUrl = shoesUrl + "/?productId=" + launchId + "&size=" + usShoesSize

    return shoesSize, launchId, skuId, productId, postpayLink

if __name__ == '__main__':
    shoesSize, launchId, skuId, productId, postpayLink = buySet(
        "https://www.nike.com/cn/launch/t/air-max-270-volt-black-oil-grey/")

    threads = int(input("根据参与用户数量自行设置一个购买和监控的线程数:"))

    userInfoList = []


    def bulkPurchase(orderQueue):
        def buy(refreshToken, username, password):
            try:
                app = BuySnkrs(refreshToken, skuId, launchId, productId, postpayLink)

                setShippingOptionsIdResponse = app.setShippingOptionsId()
                # print(setShippingOptionsIdResponse)

                setCheckoutIdResponse = app.setCheckoutId()
                # print(setCheckoutIdResponse)

                totalPrice, priceChecksum = app.getPriceChecksum()
                # print(totalPrice, priceChecksum)

                paymentToken = app.getPaymentToken(totalPrice)
                # print(paymentToken)

                launchEntrie = app.launchEntrie(paymentToken, priceChecksum)

                userInfo = [refreshToken, launchEntrie["id"], username, password]
                orderQueue.put(userInfo)
            except:
                traceback.print_exc()
            finally:
                td.release()

        conn = sqlite3.connect("nike.db")
        conn.text_factory = str
        c = conn.cursor()
        allUser = c.execute("SELECT * from nike").fetchall()

        td = threading.BoundedSemaphore(threads)
        threadlist = []
        for user in allUser:
            username = user[2]
            password = user[3]
            refreshToken = user[1]

            td.acquire()
            t = threading.Thread(target=buy, args=(refreshToken, username, password))
            t.start()
            threadlist.append(t)
        for x in threadlist:
            x.join()

        c.close()


    def orderStatus(orderQueue):
        def checkStatus(u):
            try:
                token, order, usr, pwd = u
                url = "https://unite.nikecloud.com/tokenRefresh?backendEnvironment=identity&locale=zh_CN&mobile=true&native=true&uxId=com.nike.commerce.snkrs.ios&sdkVersion=2.8.4&backendEnvironment=identity&platform=ios&browser=uniteSDK"
                data = {"client_id": "G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj", "grant_type": "refresh_token",
                        "refresh_token": token}
                r = requests.post(url, json=data).json()
                accessToken = r["access_token"]
                headers = {"authorization": "Bearer " + accessToken}
                response = requests.get("https://api.nike.com/launch/entries/v2/" + order, headers=headers).json()
                print(usr, response)
                try:
                    result = response["result"]
                except:
                    return
                if result["status"] == "WINNER":
                    print("抢购成功, 帐号:%s 密码:%s (自行登陆手机app可查看订单)" % (usr, pwd))
                    userInfoList.remove(u)
                elif result["status"] == "NON_WINNER":
                    print("%s 抢购失败" % usr)
                    userInfoList.remove(u)
            except:
                traceback.print_exc()
            finally:
                td.release()

        while True:
            if not orderQueue.empty():
                userInfo = orderQueue.get(True)
                userInfoList.append(userInfo)
            else:
                if len(userInfoList) != 0:
                    td = threading.BoundedSemaphore(threads)
                    threadlist = []
                    for u in userInfoList:
                        td.acquire()
                        t = threading.Thread(target=checkStatus, args=(u,))
                        t.start()
                        threadlist.append(t)
                    for x in threadlist:
                        x.join()
                else:
                    time.sleep(2)


    orderQueue = Queue()
    buy = Process(target=bulkPurchase, args=(orderQueue,))
    status = Process(target=orderStatus, args=(orderQueue,))
    buy.start()
    status.start()