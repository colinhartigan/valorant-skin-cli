from .config_manager import Config as app_config

from ..cli.commands.config import Config_Editor
from ..flair_loader.skin_loader import Loader

class Onboarder:

    def __init__(self,client):
        self.client = client
        self.config = Config_Editor.fetch_config()

        self.procedure = [
            {
                "text": "please select a region",
                "method": Config_Editor.set_region,
                "args": (self.config["region"]),
                "delay": "3"
            },
            {
                "text": "loading your skins..."
                "method": Loader.generate_skin_data,
                "args": (self.client)
            }
        ]

    

    # ask for region
    # load skins for first time
    # run through modifier
