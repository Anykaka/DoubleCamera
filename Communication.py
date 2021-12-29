""" 该模块主要通过UART串口接收和发送信息"""
from ctypes import *

import serial
import TakePicture
import sys
import TakePicture


def init_uart(portx="/dev/ttymxc1", bps=115200, timex=1):
    ret = 0
    dev = ""
    try:
        dev = serial.Serial(portx, bps, timeout=timex)
        if dev.isOpen():
            ret = 1
            print("serial open successfully")
    except Exception as e:
        print("---serial open error:---", e)
    return ret, dev


def close_uart(dev):
    dev.close()


def uart_receive(dev):
    if dev.in_waiting:
        inf = dev.read(dev.in_waiting).decode("utf8")
        print(inf)
        return inf


def uart_send(dev, inf):
    result = dev.write(inf.encode("utf8"))
    return result


def take_picture():
    file = CDLL('./camera.so')
    inf = file.camera(1)
    return inf


def take_picture_command(dev):
    print(uart_send(dev, "TakePicture"))
    return take_picture()
