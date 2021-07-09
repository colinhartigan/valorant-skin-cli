from InquirerPy.utils import color_print

from .config_manager import Config as app_config

from ..cli.commands.config import Config_Editor
from ..flair_loader.skin_loader import Loader
from ..flair_management.skin_manager.randomizer_editor import Editor


class Onboarder:

    def __init__(self, client):
        self.client = client
        self.config = app_config.fetch_config()

        self.procedure = [
            {
                "text": "set region:",
                "method": Config_Editor.set_region,
                "args": (self.config["region"]),
                "callback": self.update_region
            },
            {
                "text": "generating fresh skin data file...",
                "method": Loader.generate_blank_skin_file,
                "args": None
            },
            {
                "text": "loading your skins...",
                "method": Loader.generate_skin_data,
                "args": (self.client),
            },
            {
                "text": "set your skin preferences:",
                "method": Editor.select_weapon_type,
                "args": None,
            }
        ]
        self.run()

    def run(self):

        for item in self.procedure:
            returned = None
            color_print([("Green", item["text"])])
            if item["args"] is not None:
                returned = item["method"](item["args"])
            else:
                returned = item["method"]()

            if "callback" in item.keys():
                item["callback"](returned)

        self.config["meta"]["onboarding_completed"] = True
        app_config.modify_config(self.config)
        color_print([("Lime bold", "onboarding completed!")])

    def update_region(self, region):
        self.config["region"] = region
        app_config.modify_config(self.config)
