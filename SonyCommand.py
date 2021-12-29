import time

from SonyCommand_js import *
import CameraModel
import SendPost


class SonyCommand:
    model = 0
    send_post = 0

    def __init__(self, arg1):
        self.model = arg1
        self.send = SendPost.SendPost(self.model)

    def sony_command(self, command, set_value=0):
        command_result = {"default": "worry"}
        if command == "getFNumber":
            command_result = self.send.send_post(js_getFNumber)
        if command == "getAvailableFNumber":
            command_result = self.send.send_post(js_getAvailableFNumber)
        if command == "setFNumber":
            js_setFNumber["params"] = set_value
            command_result = self.send.send_post(js_setFNumber)

        if command == "getIsoSpeedRate":
            command_result = self.send.send_post(js_getIsoSpeedRate)
        if command == "getAvailableIsoSpeedRate":
            command_result = self.send.send_post(js_getAvailableIsoSpeedRate)
        if command == "setIsoSpeedRate":
            js_setIsoSpeedRate["params"] = set_value
            command_result = self.send.send_post(js_setIsoSpeedRate)

        if command == "getShutterSpeed":
            command_result = self.send.send_post(js_getShutterSpeed)
        if command == "getAvailableShutterSpeed":
            command_result = self.send.send_post(js_getAvailableShutterSpeed)
        if command == "setShutterSpeed":
            js_setShutterSpeed["params"] = set_value
            command_result = self.send.send_post(js_setShutterSpeed)

        if command == "getFocusMode":
            command_result = self.send.send_post(js_getFocusMode)
        if command == "getAvailableFocusMode":
            command_result = self.send.send_post(js_getAvailableFocusMode)
        if command == "setFocusMode":
            command_result = self.send.send_post(js_setFocusMode)

        if command == "actTakePicture":
            self.send.send_post(js_actHalfPressShutter)
            time.sleep(0.2)
            command_result = self.send.send_post(js_actTakePicture)
            self.send.send_post(js_cancelHalfPressShutter)

        if command == "startLiveview":  ###
            command_result = self.send.send_post(js_startLiveview)
        if command == "stopLiveview":  ###
            command_result = self.send.send_post(js_stopLiveview)

        return command_result

