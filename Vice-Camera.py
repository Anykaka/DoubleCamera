#!/usr/bin/python3

import Devices
import Communication
import ModelInit
import CameraModel
import threading
import SonyCommand
import inspect
import ctypes
from threading import Thread, Lock


def devices_init():
    # 加载设备驱动
    Devices.load_wifi()
    # Devices.conf_pwm()
    ret, dev = Communication.init_uart()
    return dev


def devices_close(dev):
    # 关闭设备
    # Devices.conf_pwm(enable=0)
    Devices.down_wifi()
    Communication.close_uart(dev)


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def set_f_number(set_value):                                        # 光圈槽函数
    set_value = ["%s" % set_value]
    sony_command.sony_command("setFNumber", set_value)


def set_iso_speed(set_value):                                       # 感光度槽函数
    set_value = ["%s" % set_value]
    sony_command.sony_command("setIsoSpeedRate", set_value)


def set_shutter_speed(set_value):                                   # 快门槽函数
    set_value = ["%s" % set_value]
    sony_command.sony_command("setIsoSpeedRate", set_value)


if __name__ == "__main__":
    t = Thread(target=Devices.conf_led)
    t.start()
    dev = devices_init()
    model = CameraModel.CameraModel()  # 初始化相机模型
    sony_command = SonyCommand.SonyCommand(model)  # 初始化命令对象
    ModelInit.model_init(sony_command)  # model初始化
    # 双相机初始化同步等待反馈
    while 1:
        if Communication.uart_receive(dev) == "CONNECT_RET":
            Communication.uart_send(dev, "CONNECT")
            break
    error = 0
    while 1:
        Devices.LED_BLINK = [700, 300]
        # 获取主相机指令
        inf = Communication.uart_receive(dev)
        # 从相机属性设置
        if inf == "SetViceCamera":
            Devices.LED_BLINK = [400, 100]
            Communication.uart_send(dev, "\n\rF_number: "+",".join(model.get_f_number_desc())+"\n\r")
            Communication.uart_send(dev, "\n\rISO: "+",".join(model.get_iso_speed_desc())+"\n\r")
            Communication.uart_send(dev, "\n\rShutter: "+",".join(model.get_shutter_speed_desc())+"\n\r")
            while 1:
                inf = Communication.uart_receive(dev)
                inf = str(inf).split(",")
                #  相机属性获取
                if inf[0] == 'GetSetInf':
                    if inf[1] == 'ALL':
                        Communication.uart_send(dev, "\n\rF_number: "+",".join(model.get_f_number_desc())+"\n\r")
                        Communication.uart_send(dev, "\n\rISO: "+",".join(model.get_iso_speed_desc())+"\n\r")
                        Communication.uart_send(dev, "\n\rShutter: "+",".join(model.get_shutter_speed_desc())+"\n\r")
                    elif inf[1] == 'ISO':
                        Communication.uart_send(dev, ",".join(model.get_iso_speed_desc()))
                    elif inf[1] == 'Shutter':
                        Communication.uart_send(dev, ",".join(model.get_shutter_speed_desc()))
                    elif inf[1] == 'F_number':
                        Communication.uart_send(dev, ",".join(model.get_f_number_desc()))
                # 相机属性设置
                elif inf[0] == 'ISO':
                    print(set_iso_speed(inf[1]))
                elif inf[0] == 'Shutter':
                    print(set_shutter_speed(inf[1]))
                elif inf[0] == 'F_number':
                    print(set_f_number(inf[1]))
                # 关闭
                elif inf[0] == 'Close':
                    Communication.uart_send(dev, "Close")
                    break
        # 从相机拍照及反馈
        elif inf == "TakePicture":
            ret = Communication.take_picture()
            if ret == 0:
                print("TakePictureOK")
                Communication.uart_send(dev, "TakePictureOK")
            else:
                print("TakePictureERROR")
                Communication.uart_send(dev, "TakePictureERROR")
        elif inf == "close":
            break
    Devices.LED_BLINK = [0, 0]
    stop_thread(t)
    devices_close(dev)
