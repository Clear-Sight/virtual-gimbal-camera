import logging
from .config import CONFIG
import time
def log_init():
    """ sets the configurations for logging """
    logging.basicConfig(filename=f'vgc/.logs/example.log',
            filemode='w', level=logging.INFO)
