from ...utility.config_manager import Config
from ...flair_management.skin_manager.randomizer import Skin_Randomizer
from ...flair_management.gunbuddy_manager.randomizer import Buddy_Randomizer

class Randomizer:

    def __init__(self,client):
        config = Config.fetch_config() 
        if config["skin_randomizer"]["enabled"]:
            Skin_Randomizer.randomize(client)
        if config["buddy_randomizer"]["enabled"]:
            Buddy_Randomizer.randomize(client)