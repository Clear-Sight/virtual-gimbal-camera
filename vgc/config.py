"""
loads and keeps the config for the system
"""
import json

def load_config():
    """ returns a dict of the config from config.json """
    with open("./config.json", 'r') as file:
        conf = json.load(file)
    return conf

CONFIG = load_config()
