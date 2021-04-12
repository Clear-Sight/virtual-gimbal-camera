import base64
import cv2
import zmq
from .adapter import Adapter
from ..config import CONFIG

class outputAdapter(Adapter):
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f'tcp://{CONFIG["domain"]}:7777')

    def send(self, frame):
        # ret, frame = self.camera.read()
        # BUG: not needed, done in the filter
        # frame = cv2.resize(frame, (640, 480))
        encoded, buf = cv2.imencode('.jpg', frame)
        image = base64.b64encode(buf)
        self.socket.send(image)
