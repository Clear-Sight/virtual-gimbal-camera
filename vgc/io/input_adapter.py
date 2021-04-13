from .adapter import Adapter
from ..config import CONFIG
import threading
import zmq
import json
import time
import uuid

class InputAdapter(Adapter):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.identifcation()
        self.thread = threading.Thread(target=self.main)
        self.host = "*"
        self.port = "7777"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.socket.subscribe("")
        self.cached_usr_msg = {}
        self.usr_msg = {
                "phi":0.0,
                "theta":0.0,
                "lock_on":False
            } # default


    def start(self):
        pass


    def identifcation(self):
        """
        Sends a message to the server
        for IP identifcation of the drone.
        """
        self.domain = CONFIG["domain"]
        port = "7776"
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect(f"tcp://{self.domain}:{port}")
        time.sleep(1)
        # sends MAC address to identify drone
        socket.send_string(f"drone-connected:{str(hex(uuid.getnode()))}")
        return True

    def recive(self):
        """ Receives a JSON user message """
        return self.socket.recv_json()

    def push(self):
        """
        Sends a user message to the
        pipeline for further handling
        """
        self.pipeline.push_usr_msg(self.usr_msg)

    def main(self):
        """ Continuously checks if a user message was received """
        while True:
            self.usr_msg = self.recive()
            if self.usr_msg != self.cached_usr_msg:
                self.cached_usr_msg = self.usr_msg
                self.push()
