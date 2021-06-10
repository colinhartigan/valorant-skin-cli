from ...utility.config_manager import Config

class Randomize_Skins:

    def __init__(self,manager):
        config = Config.fetch_config() 
        if config["skin_manager"]["randomize_after_each_game"]:
            manager.randomize_skins()