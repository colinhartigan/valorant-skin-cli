import json
import os

class Config:

    @staticmethod
    def fetch_config():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'config.json'))) as f:
            config = json.load(f)
            return config

    @staticmethod
    def modify_config(new_config):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'config.json', 'w'))) as f:
            json.dump(new_config, f)
            return Config.fetch_config()