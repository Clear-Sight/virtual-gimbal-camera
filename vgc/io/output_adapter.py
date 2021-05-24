"""
This is the output adapter.
This main responsibility is to send a
video stream from VGC to a revicer.

"""

import base64
import cv2
import zmq
from ..config import CONFIG
from ..log import logger


class OutputAdapter:
    """ Is given frames and sends them to the set domain """
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect(f'tcp://{CONFIG["output_domain"]}')
        logger.info(f'connect::tcp://{CONFIG["output_domain"]}')

    def send(self, frame):
        """ sends a frame to the set domain in CONFIG """
        buf = cv2.imencode('.jpg', frame)[1]
        image = base64.b64encode(buf)
        self.socket.send(image)

    def __del__(self):
        """
        destoy context for output. NOT threadsafe,
        but should only be one zmq connected so OK.
        """
        self.context.zmq_close()
