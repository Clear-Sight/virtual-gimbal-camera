import json

def load_config():
    """ returns a dict of the config from config.json """
    CONF_FILE = "./config.json"
    with open(CONF_FILE, 'r') as file:
        conf = json.load(file)
    return conf

CONFIG = load_config()
