#!/usr/bin/python3

import Devices
import Communication
import ModelInit
import CameraModel
import time
import threading
import SonyCommand
import inspect
import ctypes
from threading import Thread, Lock


def devices_init():
    # 加载设备驱动
    Devices.load_wifi()
    # Devices.conf_pwm()
    ret, dev_uart2 = Communication.init_uart()
    ret, dev_uart4 = Communication.init_uart("/dev/ttymxc3")
    return dev_uart2, dev_uart4


def devices_close(dev_uart2, dev_uart4):
    # 关闭设备
    Devices.conf_pwm(enable=0)
    Devices.down_wifi()
    Communication.close_uart(dev_uart2)
    Communication.close_uart(dev_uart4)


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


def set_f_number(set_value):  # 光圈槽函数
    set_value = ["%s" % set_value]
    return sony_command.sony_command("setFNumber", set_value)


def set_iso_speed(set_value):  # 感光度槽函数
    set_value = ["%s" % set_value]
    return sony_command.sony_command("setIsoSpeedRate", set_value)


def set_shutter_speed(set_value):  # 快门槽函数
    set_value = ["%s" % set_value]
    return sony_command.sony_command("setShutterSpeed", set_value)


if __name__ == "__main__":
    # 初始化：led、串口2、串口4、wifi、相机
    thread_led = Thread(target=Devices.conf_led)
    thread_led.start()
    dev_uart2, dev_uart4 = devices_init()
    model = CameraModel.CameraModel()  # 初始化相机模型
    sony_command = SonyCommand.SonyCommand(model)  # 初始化命令对象
    ModelInit.model_init(sony_command)  # model初始化
    # 双相机初始化同步等待反馈
    while 1:
        Communication.uart_send(dev_uart2, "CONNECT_RET")
        # Communication.uart_send(dev_uart2, ",".join(model.get_f_number_desc()))
        time.sleep(0.1)
        if Communication.uart_receive(dev_uart2) == "CONNECT":
            break
    error = 0
    wait = 0
    times = 0
    while 1:
        print("In while")
        Devices.LED_BLINK = [700, 300]
        # 主相机参数设置
        dev_uart4_inf = Communication.uart_receive(dev_uart4)
        if dev_uart4_inf == "SetHostCamera":
            Devices.LED_BLINK = [400, 100]
            Communication.uart_send(dev_uart4, "\n\rF_number: "+",".join(model.get_f_number_desc())+"\n\r")
            Communication.uart_send(dev_uart4, "\n\rISO: "+",".join(model.get_iso_speed_desc())+"\n\r")
            Communication.uart_send(dev_uart4, "\n\rShutter: "+",".join(model.get_shutter_speed_desc())+"\n\r")
            while 1:
                inf = Communication.uart_receive(dev_uart4)
                inf = str(inf).split(",")
                # 读信息：全部、iso、shutter、f_number
                if inf[0] == 'GetSetInf':
                    if inf[1] == 'ALL':
                        Communication.uart_send(dev_uart4, "\n\rF_number: "+",".join(model.get_f_number_desc())+"\n\r")
                        Communication.uart_send(dev_uart4, "\n\rISO: "+",".join(model.get_iso_speed_desc())+"\n\r")
                        Communication.uart_send(dev_uart4, "\n\rShutter: "+",".join(model.get_shutter_speed_desc())+"\n\r")
                    elif inf[1] == 'ISO':
                        Communication.uart_send(dev_uart4, "\n\rISO: "+",".join(model.get_iso_speed_desc())+"\n\r")
                    elif inf[1] == 'Shutter':
                        Communication.uart_send(dev_uart4, "\n\rShutter: "+",".join(model.get_shutter_speed_desc())+"\n\r")
                    elif inf[1] == 'F_number':
                        Communication.uart_send(dev_uart4, "\n\rF_number: "+",".join(model.get_f_number_desc())+"\n\r")
                # 参数设置：iso、shutter、f_number
                elif inf[0] == 'ISO':
                    print(set_iso_speed(inf[1]))
                elif inf[0] == 'Shutter':
                    print(set_shutter_speed(inf[1]))
                elif inf[0] == 'F_number':
                    print(set_f_number(inf[1]))
                # 退出设置
                elif inf[0] == 'Close':
                    break
        # 设置从相机参数
        elif dev_uart4_inf == "SetViceCamera":
            # 发送从相机进入设置模式
            Communication.uart_send(dev_uart2, "SetViceCamera")
            while 1:
                # 将指令传至从相机
                dev_uart4_inf = Communication.uart_receive(dev_uart4)
                if dev_uart4_inf is not None:
                    if dev_uart4_inf == "Close":
                        break
                    Communication.uart_send(dev_uart2, str(dev_uart4_inf))
        # 拍照
        print(Communication.take_picture_command(dev_uart2))
        # 等待从相机反馈
        while 1:
            inf = Communication.uart_receive(dev_uart2)
            if inf == "TakePictureOK":
                break
            elif inf == "TakePictureERROR":
                error = error + 1
                break
            else:
                wait = wait + 1
            if wait > 2:
                Devices.LED_BLINK = [100, 100]
                print("TimeOut")
                break
            time.sleep(0.5)
        time.sleep(2)
        times = times+1
        if times > 2:
            break
    Devices.LED_BLINK = [0, 0]
    stop_thread(thread_led)
    devices_close(dev_uart2, dev_uart4)
