
class CameraModel:
    def __init__(self):
        self.f_number = 0
        self.iso_speed = 0
        self.shutter_speed = 0
        self.focus_mode = 0
        self.f_number_desc = []
        self.iso_speed_desc = []
        self.shutter_speed_desc = []
        self.focus_mode_desc = []

        self.picture_url = 0
        self.live_view_url = 0

    def set_f_number(self, arg1):
        self.f_number = arg1

    def set_iso_speed(self, arg1):
        self.iso_speed = arg1

    def set_shutter_speed(self, arg1):
        self.shutter_speed = arg1

    def set_focus_mode(self, arg1):
        self.focus_mode = arg1

    def get_f_number(self):
        return self.f_number

    def get_iso_speed(self):
        return self.iso_speed

    def get_shutter_speed(self):
        return self.shutter_speed

    def get_focus_mode(self):
        return self.focus_mode

# Desc
    def set_f_number_desc(self, arg1):
        self.f_number_desc = arg1[:]

    def set_iso_speed_desc(self, arg1):
        self.iso_speed_desc = arg1[:]

    def set_shutter_speed_desc(self, arg1):
        self.shutter_speed_desc = arg1[:]

    def set_focus_mode_desc(self, arg1):
        self.focus_mode_desc = arg1[:]

    def get_f_number_desc(self):
        return self.f_number_desc

    def get_iso_speed_desc(self):
        return self.iso_speed_desc

    def get_shutter_speed_desc(self):
        return self.shutter_speed_desc

    def get_focus_mode_desc(self):
        return self.focus_mode_desc

# picture
    def set_picture_url(self, arg1):
        print("1")
        self.picture_url = arg1
        print(arg1)

    def get_picture_url(self):
        return self.picture_url

# liveView
    def set_live_view_url(self, arg1):
        self.live_view_url = arg1

    def get_live_view_url(self):
        return self.live_view_url
