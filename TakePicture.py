import SonyCommand
import CameraModel
import requests
import datetime
import threading


class TakePicture:
    def __init__(self):
        self.model = CameraModel.CameraModel()  # 临时用
        self.sony_command = SonyCommand.SonyCommand(self.model)

    def take_picture(self):
        return self.sony_command.sony_command("actTakePicture")
