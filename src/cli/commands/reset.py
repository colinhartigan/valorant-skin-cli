from ...flair_loader.skin_loader_withcheck import Skin_Loader 
from ...utility.config_manager import Config
from .reload import Reload
from InquirerPy.utils import color_print

class Reset:

    def __init__(self):
        color_print([("Green bold", "resetting")])
        Config.create_default_config()
        Reload()