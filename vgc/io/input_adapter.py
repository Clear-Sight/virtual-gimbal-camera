from .adapter import Adapter
import threading
import zmq
import json

class InputAdapter(Adapter):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.thread = threading.Thread(target=self.main)
        self.host = "*"
        self.port = "7777"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind(f"tcp://{self.host}:{self.port}")
        self.socket.subscribe("")
        self.usr_msg = {}

    def start(self):
        pass

    def recive(self):
        return self.socket.recv_json()

    def main(self):
        while True:
            self.usr_msg = self.recive()
