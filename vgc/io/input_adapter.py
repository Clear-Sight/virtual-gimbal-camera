from ..config import CONFIG
import threading
import zmq
import json
import time
import uuid
import requests

class InputAdapter:
    """
    Fetches the user input from server
    and pushes it over pipeline to view_controller
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.thread = threading.Thread(target=self.main)
        self.usr_msg = {"compass":0.0, "angle":90.0, "zoom":2,"lock_on":False}
        self.cached_usr_msg = {"compass":0.0, "angle":90.0, "zoom":2,"lock_on":False}

    def start(self):
        """ thread starting funciton """
        self.thread.start()


    def get_usr_input(self):
        """ Fetch user input from web server via GET request. """
        try:
            r = requests.get(
            f'http://{CONFIG["input_domain"]}/drone/user/fetch')
            return r.json()
        except:
            return self.cached_usr_msg

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
            time.sleep(CONFIG["input_check_frequency"]) # maybe should be something better
