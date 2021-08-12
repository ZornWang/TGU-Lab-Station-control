import json
import socket

address = ('192.168.1.19', 31500)  # 服务端地址和端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    trigger = input('Input: ')
    data = {
        'action_id': 1,
        'user_id': 1
    }
    s.sendto(json.dumps(data).encode(), address)
    # s.sendto(trigger.encode(), address)
    if trigger == '###':  # 自定义结束字符串
        break
s.close()