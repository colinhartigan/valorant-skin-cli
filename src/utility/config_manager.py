import json
import os

class Config:

    @staticmethod
    def fetch_config():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'config.json'))) as f:
            config = json.load(f)
            return config