#coding=utf-8
import json
import socket
import ssl
import traceback,time
import uuid
import requests
from WebLogin import WebLogin_Chrome



class LoginInit:
    def __init__(self, username, password):
        self.username = "+86" + username
        self.password = password

        self.host = "s3.nikecdn.com"
        self.visitorId = str(uuid.uuid4())
        self.clientId = "G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj"
        self.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79"

        webLogin = WebLogin_Chrome(username, password)
        webLogin.login()
        self.cookies = webLogin.getCookies()

    # 获取app登陆请求
    def getLoginRequests(self):
        payload = '{{"username":"{usr}","password":"{pwd}","client_id":"{clientId}","ux_id":"com.nike.commerce.snkrs.ios","grant_type":"password"}}'.format(
            usr=self.username, pwd=self.password, clientId=self.clientId)

        head = '''POST /login?appVersion=454&experienceVersion=375&uxid=com.nike.commerce.snkrs.ios&locale=zh_CN&backendEnvironment=identity&browser=Apple%20Computer%2C%20Inc.&os=undefined&mobile=true&native=true&visit=1&visitor={visitorId} HTTP/1.1
Host: {host}
Content-Type: application/json
Origin: https://{host}
Cookie: {cookies}
Content-Length: {length}
Connection: close
Accept: */*
User-Agent: {userAgent}
Referer: https://s3.nikecdn.com/unite/mobile.html?mid=66794190406425515927935901233201301138?iOSSDKVersion=2.8.4&clientId=G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj&uxId=com.nike.commerce.snkrs.ios&view=none&locale=zh_CN&backendEnvironment=identity
Accept-Language: zh-cn'''.format(visitorId=self.visitorId, host=self.host, userAgent=self.userAgent,
                                 length=len(payload), cookies=self.cookies)

        data = head + "\r\n\r\n" + payload
        return data

    def getDataFromResponse(self, data):
        data = json.loads(data.split("\r\n\r\n")[1])
        return data

    # 发送请求
    def sendRequestsToHost(self, data):
        sock = ssl.wrap_socket(socket.socket())
        sock.connect((self.host, 443))

        sock.sendall(bytes(data, encoding='utf-8'))
        # recv_data = sock.recv(10240).decode('utf-8')
        result = ""
        while True:
            try:
                recv_data = sock.recv(2048)
                result += recv_data.decode('utf-8')
            except socket.error as err_msg:
                print('Error receiving data: %s' % err_msg)
            if not len(recv_data):
                break
        sock.close()
        return result

#ceshi=LoginInit('15245871026','huanxiangmf1Q')
#print (ceshi.sendRequestsToHost(data=ceshi.getLoginRequests()))

class BuySnkrs:
    def __init__(self, refreshToken, skuId, launchId, productId, postpayLink):
        self.refreshToken = refreshToken

        self.skuId = skuId
        self.launchId = launchId
        self.productId = productId
        self.postpayLink = postpayLink

        self.host = "s3.nikecdn.com"
        self.apiHost = "api.nike.com"
        self.visitorId = str(uuid.uuid4())
        self.clientId = "G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj"
        self.userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79"

        self.apiUserAgent = "SNKRS/3.3.3 (iPhone; iOS 11.4; Scale/2.00)"
        self.xNewRelicID = "VQYGVF5SCBADUVBRBgAGVg=="
        self.xNikeCallerId = "nike:snkrs:ios:3.3"

        self.checkoutId = str(uuid.uuid4())
        self.shippingId = str(uuid.uuid4())
        self.paymentsId = str(uuid.uuid4())

        self.times = self.getUtcTime()

        self.token = self.getTokenRefresh()

        # 格式化一些购买过程中所需的参数
        self.userCommerce = self.getUserCommerce()
        self.email = self.userCommerce["emails"]["primary"]["email"]

        # print(self.userCommerce["address"])
        # for i in self.userCommerce["address"]:
        #     address = self.userCommerce["address"][i]
        #     break
        address = self.userCommerce["address"]["shipping"]
        state = address["province"]
        city = address["locality"]
        county = address["zone"]
        address1 = address["line1"]
        try:
            address2 = address["line2"]
        except:
            address2 = " "
        postalCode = address["code"]
        country = address["country"]
        self.addressInfo = {"state": state, "city": city, "address1": address1, "postalCode": postalCode,
                            "address2": address2, "county": county, "country": country}

        name = address["name"]["primary"]
        lastName = name["given"]
        firstName = name["family"]
        self.recipientInfo = {"lastName": lastName, "firstName": firstName}

        phone = address["phone"]["primary"]
        self.contactInfo = {"phoneNumber": phone, "email": self.email}

        # 格式化最终抢购所需的参数
        self.launchRecipient = {"lastName": lastName, "firstName": firstName, "email": self.email,
                                "phoneNumber": phone}

        self.launchAddress = {"state": state, "city": city, "address1": address1, "county": county, "country": "CN"}

    # 获取服务器时区的时间
    def getUtcTime(self):
        utcTime = time.gmtime()
        return utcTime

    # 获取最新发布的产品
    def gwtProductFeed(self):
        response = requests.get(
            "https://api.nike.com/commerce/productfeed/products/snkrs/threads?country=CN&limit=5&locale=zh_CN&skip=0&withCards=true").json()
        return response

    # 获取新的通知信息
    def getNotifications(self):
        times = time.strftime("%Y-%m-%dT%H%%3A%M%%3A%S.000%%2B0000", self.times)
        url = "https://api.nike.com/plus/v3/notifications/me/stored?since={time}&limit=10&locale=zh-Hans_CN".format(
            time=times)
        headers = {
            "deliveryId": "com.nike.onenikecommerce",
            "appid": "com.nike.commerce.snkrs.ios",
            "Authorization": "Bearer " + self.token,
            "User-Agent": self.apiUserAgent,
            "X-NewRelic-ID": self.xNewRelicID
        }
        response = requests.get(url, headers=headers).json()
        return response

    # 获取订单信息
    def getOrderHistory(self):
        url = "https://api.nike.com/commerce/ap/orderhistory?action=getOrderHistoryList&country=CN"
        headers = {
            "X-NewRelic-ID": self.xNewRelicID,
            "User-Agent": self.apiUserAgent,
            "Authorization": "Bearer " + self.token
        }
        response = requests.get(url, headers=headers).text
        return response

    # 刷新登陆凭证
    def getTokenRefresh(self):
        url = "https://unite.nikecloud.com/tokenRefresh?backendEnvironment=identity&locale=zh_CN&mobile=true&native=true&uxId=com.nike.commerce.snkrs.ios&sdkVersion=2.8.4&backendEnvironment=identity&platform=ios&browser=uniteSDK"
        data = {"client_id": self.clientId, "grant_type": "refresh_token",
                "refresh_token": self.refreshToken}
        r = requests.post(url, json=data).json()
        return r["access_token"]

    # 获取用户基本信息
    def getUserCommerce(self):
        url = "https://api.nike.com/user/commerce"
        headers = {
            "X-NewRelic-ID": self.xNewRelicID,
            "User-Agent": self.apiUserAgent,
            "Authorization": "Bearer " + self.token,
            "X-NIKE-UX-ID": "com.nike.commerce.snkrs.ios"
        }
        response = requests.get(url, headers=headers).json()
        return response

    def setShippingOptionsId(self):
        url = "https://api.nike.com/buy/shipping_options/v2"
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json; charset=utf-8",
            "x-nike-caller-id": self.xNikeCallerId,
            "User-Agent": self.apiUserAgent,
            "X-NewRelic-ID": self.xNewRelicID
        }
        data = {"items": [{"id": self.shippingId, "shippingAddress": self.addressInfo, "skuId": self.skuId}],
                "currency": "CNY", "country": "CN"}
        response = requests.post(url, headers=headers, json=data).json()
        return response

    def setCheckoutId(self):
        url = "https://api.nike.com/buy/checkout_previews/v2/" + self.checkoutId
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "x-nike-caller-id": self.xNikeCallerId,
            "User-Agent": self.apiUserAgent,
            "X-NewRelic-ID": self.xNewRelicID
        }
        data = {"request": {"email": self.email,
                            "clientInfo": {"deviceId": "", "client": "com.nike.commerce.snkrs.ios"}, "currency": "CNY",
                            "items": [{"recipient": self.recipientInfo,
                                       "shippingAddress": self.addressInfo,
                                       "id": self.shippingId, "quantity": 1,
                                       "skuId": self.skuId,
                                       "shippingMethod": "GROUND_SERVICE",
                                       "contactInfo": self.contactInfo}],
                            "channel": "SNKRS", "locale": "zh_CN", "country": "CN"}}
        response = requests.put(url, headers=headers, json=data).json()
        return response

    def getPriceChecksum(self):
        url = "https://api.nike.com/buy/checkout_previews/v2/jobs/" + self.checkoutId
        headers = {
            "Accept": "application/json",
            "X-NewRelic-ID": self.xNewRelicID,
            "x-nike-caller-id": self.xNikeCallerId,
            "Authorization": "Bearer " + self.token,
            "User-Agent": self.apiUserAgent
        }
        response = requests.get(url, headers=headers).json()
        totalPrice = response["response"]["totals"]["total"]
        priceChecksum = response["response"]["priceChecksum"]
        return totalPrice, priceChecksum

    def getPaymentToken(self, totalPrice):
        url = "https://api.nike.com/payment/preview/v2"
        headers = {
            "Accept": "application/json; charset=utf-8",
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "x-nike-caller-id": self.xNikeCallerId,
            "User-Agent": self.apiUserAgent,
            "X-NewRelic-ID": self.xNewRelicID
        }
        data = {"total": totalPrice, "items": [{"productId": self.productId,
                                                "shippingAddress": self.addressInfo}],
                "checkoutId": self.checkoutId, "currency": "CNY", "paymentInfo": [
                {"id": self.paymentsId, "type": "Alipay",
                 "billingInfo": {"name": self.recipientInfo,
                                 "contactInfo": self.contactInfo,
                                 "address": self.addressInfo}}], "country": "CN"}
        response = requests.post(url, headers=headers, json=data).json()
        paymentToken = response["id"]
        return paymentToken

    def getDataFromResponse(self, data):
        data = json.loads(data.split("\r\n\r\n")[1])
        return data

    # 发送请求
    def sendRequestsToHost(self, data):
        sock = ssl.wrap_socket(socket.socket())
        sock.connect((self.host, 443))

        sock.sendall(bytes(data, encoding='utf-8'))
        # recv_data = sock.recv(10240).decode('utf-8')
        result = ""
        while True:
            try:
                recv_data = sock.recv(2048)
                result += recv_data.decode('utf-8')
            except socket.error as err_msg:
                print('Error receiving data: %s' % err_msg)
            if not len(recv_data):
                break
        sock.close()
        return result

    def sendRequestsToApiHost(self, data):
        sock = ssl.wrap_socket(socket.socket())
        sock.connect((self.apiHost, 443))

        sock.sendall(bytes(data, encoding='utf-8'))
        # recv_data = sock.recv(10240)
        result = ""
        while True:
            try:
                recv_data = sock.recv(2048)
                result += recv_data.decode('utf-8')
            except socket.error as err_msg:
                print('Error receiving data: %s' % err_msg)
            if not len(recv_data):
                break
        sock.close()
        return result

    def launchEntrie(self, paymentToken, priceChecksum):
        url = "https://api.nike.com/launch/entries/v2"
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "x-nike-caller-id": self.xNikeCallerId,
            "User-Agent": self.apiUserAgent,
            "X-NewRelic-ID": self.xNewRelicID
        }
        data = {"deviceId": "", "postpayLink": self.postpayLink, "checkoutId": self.checkoutId, "currency": "CNY",
                "paymentToken": paymentToken,
                "shipping": {"recipient": self.launchRecipient, "method": "GROUND_SERVICE",
                             "address": self.launchAddress}, "skuId": self.skuId, "channel": "SNKRS",
                "launchId": self.launchId, "locale": "zh_CN", "priceChecksum": priceChecksum}
        response = requests.post(url, headers=headers, json=data).json()
        return response