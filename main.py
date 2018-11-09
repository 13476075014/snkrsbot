#coding=utf-8
from a1 import *
from a2 import *
from login import *
from WebLogin import *
if __name__ == '__main__':
    shoesSize, launchId, skuId, productId, postpayLink = buySet(
        "https://www.nike.com/cn/launch/t/air-revaderchi-gym-red-mink-brown/")

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