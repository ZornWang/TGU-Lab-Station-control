# coding=utf-8

import time
import control
import Accept
import threading
import RPi.GPIO as GPIO
import Adafruit_DHT

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pin_trig = 3
pin_echo = 2
GPIO.setup(pin_trig, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(pin_echo, GPIO.IN)
time.sleep(1)

sensor = Adafruit_DHT.DHT22
pin = 20

CHANNEL = 26
GPIO.setup(CHANNEL,GPIO.IN)

ExistFlag = 0
LightFlag = 0
FansFLag = 0
HumiFlag = 0

class isExist(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        exist()

def check():
    # 发出触发信号
    GPIO.output(pin_trig, GPIO.HIGH)
    # 保持一段时间
    time.sleep(0.1)
    GPIO.output(pin_trig, GPIO.LOW)

    while not GPIO.input(pin_echo):
        pass
    # 发现高电平开始计时
    t1 = time.time()

    while GPIO.input(pin_echo):
        pass

    # 高电平结束停止计时
    t2 = time.time()
    # 返回距离
    return (t2 - t1) * 340 / 2


def exist():
    global ExistFlag
    global LightFlag
    global FansFLag
    global HumiFlag
    time1 = 0
    time2 = 0
    time3 = 0
    while True:
        if ExistFlag != 0:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None and time.time()-time1>=5:
                time1 = time.time()
                if round(temperature) <= 19.0 and FansFLag == 1:
                    print('当前温度：{0:0.1f}*C'.format(temperature))
                    control.fans_close(Accept.getUser_id())
                    FansFLag = 0
                if round(temperature) >= 24.0 and FansFLag == 0:
                    print('当前温度：{0:0.1f}*C'.format(temperature))
                    control.fans_open(Accept.getUser_id())
                    FansFLag = 1
                if round(humidity) <= 30.0 and HumiFlag == 0:
                    print('当前湿度：{0:0.1f}%'.format(humidity))
                    HumiFlag = 1
                if round(humidity) >= 80.0 and HumiFlag == 1:
                    print('当前湿度：{0:0.1f}%'.format(humidity))
                    HumiFlag = 0
                # time.sleep(5)

            if GPIO.input(CHANNEL) == True and time.time()-time2>=1 and LightFlag == 0:
                time2 = time.time()
                print(str(Accept.getUser_id())+'号工位光线不足，开灯')
                control.light_open(Accept.getUser_id())
                LightFlag = 1
            # 光照充足关灯，暂时取消这一功能，避免死锁
            # if GPIO.input(CHANNEL) == False and time.time()-time2>=1 and LightFlag == 1:
            #     time2 = time.time()
            #     # time.sleep(5)
            #     if GPIO.input(CHANNEL) == False:
            #         print(str(Accept.getUser_id())+'号工位光线充足，关灯')
            #         control.light_close(Accept.getUser_id())
            #         LightFlag = 0



            #人暂离
            if check()>1.00 and check()<5.00 and ExistFlag == 1:
                time.sleep(3)
                #设置暂离时间多久后断电
                if check()>1.00 and check()<5.00:
                    print(str(Accept.getUser_id())+'号工位人员离开实验室')
                    ExistFlag = 0
                    LightFlag = 0
                    FansFLag = 0
                    HumiFlag = 0
                    control.light_close(Accept.getUser_id())
                    control.fans_close(Accept.getUser_id())
        # 人回来
        elif check() < 1.00 and ExistFlag == 0:
            time.sleep(3)
            if check() < 1.00:
                ExistFlag = 1
                Accept.user_id = 1