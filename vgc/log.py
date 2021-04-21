import logging
from .config import CONFIG
from datetime import datetime
def log_init():
    """ sets the configurations for logging """

    date = datetime.now().strftime("%m-%d-%Y")
    if CONFIG["debug"]:
        logging.basicConfig(filename=f'vgc/.logs/vgc-{date}.log',
            filemode='w', level=logging.DEBUG)
    else:
        logging.basicConfig(filename=f'vgc/.logs/vgc-{date}.log',
            filemode='w', level=logging.INFO)
