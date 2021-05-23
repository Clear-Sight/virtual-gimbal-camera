"""
input adapter contains class InputAdapter
that featches messages from server
"""

import threading
import time
import requests
from requests.exceptions import HTTPError
from ..log import logger
from ..config import CONFIG

class InputAdapter:
    """
    Fetches the user input from server
    and pushes it over pipeline to view_controller
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.thread = threading.Thread(target=self.main)
        self.DEFAULT_USR_MSG = {"compass":0.0, "angle":0.0,\
                                "zoom":2,"lock_on":False}
        self.usr_msg = {"compass":0.0, "angle":0.0,\
                            "zoom":2,"lock_on":False}
        self.cached_usr_msg = {}

    def start(self):
        """ thread starting funciton """
        self.thread.start()


    def get_usr_input(self):
        """ Fetch user input from web server via GET request. """
        self.usr_msg = self.DEFAULT_USR_MSG
        try:
            req = requests.get(
                f'http://{CONFIG["input_domain"]}/drone/user/fetch')
        except HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
        else:
            self.usr_msg = req.json()
        if list(self.usr_msg.keys()) != list(self.DEFAULT_USR_MSG.keys()):
            logger.error(f'bad usr msg keys:{list(self.usr_msg.keys())}')
            self.usr_msg = self.DEFAULT_USR_MSG
        return self.usr_msg

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
            time.sleep(CONFIG["input_check_frequency"])
            # maybe should be something better
