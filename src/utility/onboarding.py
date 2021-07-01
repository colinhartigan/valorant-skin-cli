from .config_manager import Config as app_config

from ..cli.commands.config import Config_Editor

class Onboarder:

    def __init__(self):
        self.config = Config.fetch_config()

    