"""
This is the output adapter.
This main responsibility is to send a
video stream from VGC to a revicer.

"""

import base64
import cv2
import zmq
from ..config import CONFIG



class OutputAdapter:
    """ Is given frames and sends them to the set domain """
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f'tcp://{CONFIG["output_domain"]}')

    def send(self, frame):
        """ sends a frame to the set domain in CONFIG """
        buf = cv2.imencode('.jpg', frame)[1]
        image = base64.b64encode(buf)
        self.socket.send(image)

    def __del__(self):
        self.socket.__del__()
