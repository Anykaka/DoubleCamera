import requests
from queue import Queue
import SonyCommand
import CameraModel


class VideoPlayer:
    def __init__(self, picture_queue):
        self.model = CameraModel.CameraModel()  # 临时用
        self.sony_command = SonyCommand.SonyCommand(self.model)
        self.picture_queue = picture_queue

    def video_player(self):  # 从相机获取图片并保存到队列里  A线程函数
        self.sony_command.sony_command("startLiveview")
        evf_url = self.model.get_live_view_url()
        evf_data = requests.get(evf_url, stream=True)
        while True:
            evf_data.raw.read(12)
            temp = evf_data.raw.read(3)  # 图片字节大小
            temp = int.from_bytes(temp, 'big')
            evf_data.raw.read(121)
            picture_byte = evf_data.raw.read(temp)
            if self.picture_queue.qsize() == 2:  # 若没有及时取出图片，则删除一张
                self.picture_queue.get()
            self.picture_queue.put(picture_byte)