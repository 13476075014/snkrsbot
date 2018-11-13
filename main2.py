#coding=utf-8
from loginnk import *
import re
import requests
from WebLoginnk import *
import threading,sqlite3,time
from multiprocessing import Process
from multiprocessing import Queue

def partdraw(chouqian):

    print("nihao")
conn = sqlite3.connect("nike.db")
conn.text_factory = str
c = conn.cursor()
allUser = c.execute("SELECT * from nike").fetchall()
for user in allUser:
    username = user[2]
    password = user[3]
    refreshToken = user[1]
    # print("%s  %s  %s",username,password,refreshToken)
    #参与抽签
    partdraw()
c.close()
