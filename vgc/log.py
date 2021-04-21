import logging
from .config import CONFIG
from datetime import datetime


date = datetime.now().strftime("%m-%d-%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler(f'vgc/.logs/vgc-{date}.log')
logger.addHandler(file_handler)
