from InquirerPy.utils import color_print
from valclient.client import Client
import time

from .config_manager import Config as app_config

from ..cli.commands.reload import Reload
from ..flair_loader.skin_loader_withcheck import Skin_Loader

from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..flair_management.loadout_manager.loadouts_manager import Loadouts_Manager
from ..flair_management.skin_manager.randomizer_editor import Editor


class Onboarder:

    def __init__(self):
        self.config = app_config.fetch_config()
        self.client = Client(region="na" if self.config['region'][0] == "" else self.config['region'][0])
        self.client.activate()

        self.procedure = [
            {
                "text": "autodetecting region",
                "method": self.autodetect_region,
                "args": None,
            },
            {
                "text": "generating fresh skin data file...",
                "method": Skin_Manager.generate_blank_skin_file,
                "args": None
            },
            {
                "text": "generating blank loadouts file...",
                "method": Loadouts_Manager.generate_blank_loadouts_file,
                "args": None
            },
            {
                "text": "loading your skins...",
                "method": Skin_Loader.generate_skin_data,
                "args": (self.client,),
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
                returned = item["method"](*item["args"])
            else:
                returned = item["method"]()

            if "callback" in item.keys():
                item["callback"](returned)

        self.config["meta"]["onboarding_completed"] = True
        app_config.modify_config(self.config)
        color_print([("Lime bold", "onboarding completed!")])


    def autodetect_region(self):
        if self.config["region"][0] == "":
            client = Client(region="na")
            client.activate()
            sessions = client.riotclient_session_fetch_sessions()
            for _,session in sessions.items():
                if session["productId"] == "valorant":
                    launch_args = session["launchConfiguration"]["arguments"]
                    for arg in launch_args:
                        if "-ares-deployment" in arg:
                            region = arg.replace("-ares-deployment=","")
                            self.config["region"][0] = region
                            app_config.modify_config(self.config)
                            color_print([("LimeGreen",f"autodetected region: {self.config['region'][0]}")])
                            Reload()
        else:
            color_print([("LimeGreen",f"region: {self.config['region'][0]}")])