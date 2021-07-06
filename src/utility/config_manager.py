import json
import os
from InquirerPy.utils import color_print
from .filepath import Filepath

class Config:

    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json'))) as f:
                config = json.load(f)
                return config
        except:
            #color_print([("Yellow bold", f"[!] integrity check of config file failed; generating fresh config")])
            return Config.create_blank_config()

    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(new_config, f)

        return Config.fetch_config()

    @staticmethod
    def create_blank_config():
        config = {
            "region": "na",
            "async_refresh_interval": 5,
            "skin_manager": {
                "randomize_after_each_game": True
            },
            "meta": {
                "onboarding_completed": False
            }
        }
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'config.json')), 'w') as f:
            json.dump(config, f)
        return Config.fetch_config()
