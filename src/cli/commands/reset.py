from ...flair_loader.skin_loader_withcheck import Loader 
from ...utility.config_manager import Config
from .reload import Reload
from InquirerPy.utils import color_print

class Reset:

    def __init__(self,client):
        color_print([("Green bold", "resetting")])
        Config.create_default_config()
        Reload()