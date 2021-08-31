import json
import os
from .filepath import Filepath
from valclient import Client

default_config = {
    "version": "v1.3.0b2",
    "region": ["",Client.fetch_regions()],
    "async_refresh_interval": 5,
    "skin_randomizer": {
        "enabled": True
    },
    "buddy_randomizer": {
        "enabled": True,
    },
    "meta": {
        "onboarding_completed": False,
        "surpress_update_notifications": False,
    }
}

class Config:

    @staticmethod
    def fetch_config():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json"))) as f:
                config = json.load(f)
                return config
        except:
            return Config.create_default_config()

    @staticmethod
    def modify_config(new_config):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(new_config, f)

        return Config.fetch_config()

    @staticmethod
    def check_config():
        # ???????
        # my brain hurts
        # i bet theres a way better way to write this but im just braindead
        config = Config.fetch_config()
        
        def check_for_new_vars(blank,current):
            for key,value in blank.items():
                if not key in current.keys():
                    current[key] = value
                if type(value) != type(current[key]):
                    # if type of option is changed
                    current[key] = value
                if key == "version": 
                    # version can't be changed by the user lmao
                    current[key] = value
                if key == "region": 
                    current[key][1] = Client.fetch_regions() # update regions jic ya know
                if isinstance(value,list):
                    current[key][1] = blank[key][1]
                if isinstance(value,dict):
                    check_for_new_vars(value,current[key])
            
        def remove_unused_vars(blank,current):
            def check(bl,cur):
                for key,value in list(cur.items()):
                    if not key in bl.keys():
                        del cur[key]
                    if isinstance(value,dict) and key in list(cur.keys()):
                        check(bl[key],value)

            check(blank,current)
            return current

        check_for_new_vars(default_config,config)
        config = remove_unused_vars(default_config,config)
        Config.modify_config(config)

    @staticmethod
    def create_default_config():
        if not os.path.exists(Filepath.get_appdata_folder()):
            os.mkdir(Filepath.get_appdata_folder())
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), "config.json")), "w") as f:
            json.dump(default_config, f)
        return Config.fetch_config() 
