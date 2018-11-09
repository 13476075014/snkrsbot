#coding=utf-8
import json
import socket
import ssl
import traceback
import uuid

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