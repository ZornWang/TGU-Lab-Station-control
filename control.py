# coding=utf-8
import RPi.GPIO as GPIO

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([27,22], GPIO.OUT)

def light_open(user_id):
    init()
    GPIO.output(22, 0)
    print(str(user_id)+"号工位灯打开")
    GPIO.output(22,1)

def light_close(user_id):
    init()
    GPIO.output(22, 0)
    print(str(user_id)+"号工位灯关闭")

def fans_open(user_id):
    init()
    GPIO.output(27, 0)
    print(str(user_id)+"号工位风扇打开")
    GPIO.output(27, 1)

def fans_close(user_id):
    init()
    GPIO.output(27, 0)
    print(str(user_id)+"号工位风扇关闭")