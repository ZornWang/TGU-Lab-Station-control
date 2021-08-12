# coding=utf-8
import json
import socket
import threading
import isExist

user_id = 0

dict = {'1':'陈鸿飞','2':'王准衡','3':'张涵'}

class accept(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("start accepting user's id")
        accept_user()
        print("end")


def accept_user():
    global user_id
    address = ('0.0.0.0', 31500)  # 服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)  # 绑定服务端地址和端口
    while True:
        data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址
        data = data.decode()
        if not data:
            break
        data_decoded = json.loads(data)
        if data_decoded['user_id'] == 1:
            print(str(data_decoded['user_id'])+'号工位人员进入实验室')
            user_id = data_decoded['user_id']
            isExist.ExistFlag = 1
            isExist.LightFlag = 0
            isExist.FansFLag = 0
            isExist.HumiFlag = 0
    s.close()

def getUser_id():
    return user_id