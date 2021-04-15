from .adapter import Adapter
from ..config import CONFIG
import threading
import zmq
import json
import time
import uuid
import requests

class InputAdapter(Adapter):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.thread = threading.Thread(target=self.main)
        self.port = "24474"
        self.usr_msg = {"compass":0.0, "angle":90.0, "lock_on":False}
        self.cached_usr_msg = {}

    def start(self):
        self.thread.start()


    def get_usr_input(self):
        """ Fetch user input from web server via GET request. """
        r = requests.get(
        f'http://{CONFIG["domain"]}:{self.port}/drone/user/fetch')
        return r.json()

    def push(self):
        """
        Sends a user message to the
        pipeline for further handling
        """
        self.pipeline.push_usr_msg(self.usr_msg)

    def main(self):
        """ Continuously checks if a user message was received """
        while True:
            self.usr_msg = self.get_usr_input()
            if self.usr_msg != self.cached_usr_msg:
                self.cached_usr_msg = self.usr_msg
                self.push()
            time.sleep(1) # maybe should be something better
