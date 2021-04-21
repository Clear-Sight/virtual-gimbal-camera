import logging
import os
from .config import CONFIG
from datetime import datetime


date = datetime.now().strftime("%m-%d-%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
log_filename = f'vgc/.logs/vgc-{date}.log'
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
