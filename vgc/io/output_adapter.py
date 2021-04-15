import base64
import cv2
import zmq
from .adapter import Adapter
from ..config import CONFIG

"""
This is the output adapter.
This main responsibility is to send a video stream from VGC to a revicer.

"""

class OutputAdapter(Adapter):
    """ Is given frames and sends them to the set domain """
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f'tcp://{CONFIG["domain"]}:{CONFIG["videostream_port"]}')

    def send(self, frame):
        """ sends a frame to the set domain in CONFIG """
        encoded, buf = cv2.imencode('.jpg', frame)
        image = base64.b64encode(buf)
        self.socket.send(image)
