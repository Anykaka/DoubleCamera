""" 设备驱动管理模块，提供设备驱动的加载、解除与配置 """

import os
import time
from ctypes import *
import serial

LED_BLINK = [500, 500]


# 设备加载
def load_wifi(version="rtl8188eus"):
    if version == "RTL8188EUS" or version == "rtl8188eus":
        os.system("./load/rtl8188eus.sh")
    elif version == "RTL8189FS" or version == "rtl8189fs":
        os.system("./load/rtl8189fs.sh")
    elif version == "RTL8192CU" or version == "rtl8192cu":
        os.system("./load/rtl8192cu.sh")
    else:
        print("No this wifi version.")


# 解除设备
def down_wifi(version='rtl8188eus'):
    if version == 'RTL8188EUS' or version == 'rtl8188eus':
        os.system('./down/rtl8188eus.sh')
    if version == 'RTL8189FS' or version == 'rtl8189fs':
        os.system('./down/rtl8189fs.sh')
    if version == 'RTL8192CU' or version == 'rtl8192cu':
        os.system('./down/rtl8192cu.sh')
    else:
        print("No this wifi version.")


# 设备配置
def conf_pwm(pwm='pwmchip1', period=200000, duty_cycle=100000, enable=1):
    os.system("echo 0 > /sys/class/pwm/%s/export" % pwm)
    os.system("echo %d > /sys/class/pwm/%s/pwm0/period" % (period, pwm))
    os.system("echo %d > /sys/class/pwm/%s/pwm0/duty_cycle" % (duty_cycle, pwm))
    os.system("echo %d > /sys/class/pwm/%s/pwm0/enable" % (enable, pwm))


def conf_led():
    global LED_BLINK
    print('set led state')
    while 1:
        file = CDLL('./led.so')
        ret = file.led(LED_BLINK[0], LED_BLINK[1])
