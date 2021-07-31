from ...flair_loader.skin_loader_withcheck import Skin_Loader 
from ...utility.config_manager import Config
from .reload import Reload
from InquirerPy.utils import color_print
from InquirerPy import inquirer 

class Reset:

    def __init__(self):
        confirm = inquirer.confirm(message=f"are you sure you want to reset VALORANT-skin-cli to its defaults?", default=False).execute()
        if confirm:
            color_print([("Green bold", "resetting")])
            Config.create_default_config()
            Reload()