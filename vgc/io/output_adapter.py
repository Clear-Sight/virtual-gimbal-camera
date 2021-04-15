import base64
import cv2
import zmq
from ..config import CONFIG

"""
This is the output adapter.
This main responsibility is to send a video stream from VGC to a revicer.

"""

class OutputAdapter:
    """ Is given frames and sends them to the set domain """
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f'tcp://{CONFIG["output_domain"]}')

    def send(self, frame):
        """ sends a frame to the set domain in CONFIG """
        encoded, buf = cv2.imencode('.jpg', frame)
        image = base64.b64encode(buf)
        self.socket.send(image)
