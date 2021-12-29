import json
import sys
import socket
import requests
import CameraModel
import ErrorTable

CameraHost = "http://192.168.122.1:10000/sony/camera"


class SendPost:
    model = 0

    def __init__(self, arg1):
        self.model = arg1

    def send_post(self, command_js):
        try:
            r = None
            print("command_js start:", command_js)
            r = requests.post(CameraHost, json.dumps(command_js), timeout=10)
            camera_response = json.loads(r.content.decode("utf8"))
            print("command_js end:", command_js)
            if "error" in camera_response:
                return {"error": ErrorTable.err_table(camera_response["error"][0])}
            else:
                if command_js["method"] == "getFNumber":
                    self.model.set_f_number(camera_response["result"][0])
                if command_js["method"] == "getIsoSpeedRate":
                    self.model.set_iso_speed(camera_response["result"][0])
                if command_js["method"] == "getShutterSpeed":
                    self.model.set_shutter_speed(camera_response["result"][0])
                if command_js["method"] == "getFocusMode":
                    self.model.set_focus_mode(camera_response["result"][0])

                if command_js["method"] == "getAvailableFNumber":
                    self.model.set_f_number_desc(camera_response["result"][1])
                if command_js["method"] == "getAvailableIsoSpeedRate":
                    self.model.set_iso_speed_desc(camera_response["result"][1])
                if command_js["method"] == "getAvailableShutterSpeed":
                    self.model.set_shutter_speed_desc(camera_response["result"][1])
                if command_js["method"] == "getAvailableFocusMode":
                    self.model.set_focus_mode_desc(camera_response["result"][1])

                if command_js["method"] == "setFNumber" or "setIsoSpeedRate" or "setShutterSpeed" or "stopLiveview":
                    pass

                if command_js["method"] == "actTakePicture":
                    print("actTakePicture : 1")
                    self.model.set_picture_url(camera_response["result"][0][0])

                if command_js["method"] == "startLiveview":
                    self.model.set_live_view_url(camera_response["result"][0])
                return {"command_ok": command_js}
        except:
            return {"link_error": command_js}

