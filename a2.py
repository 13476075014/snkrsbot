#coding=utf-8
import json
import re
import requests


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