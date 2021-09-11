from InquirerPy.utils import color_print
from InquirerPy import inquirer
from valclient.client import Client
import time

from .config_manager import Config as app_config

from ..cli.commands.reload import Reload
from ..cli.commands.set_skin import Set_Skin
from ..flair_loader.skin_loader import Skin_Loader

from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..flair_management.loadout_manager.loadouts_manager import Loadouts_Manager
from ..flair_management.skin_manager.randomizer_editor import Randomizer_Editor


class Onboarder:

    def __init__(self):
        self.config = app_config.fetch_config()
        try:
            self.client = Client(region=self.config['region'][0])
        except ValueError:
            self.autodetect_region()
        self.client = Client(region="na" if self.config['region'][0] == "" else self.config['region'][0])
        self.client.activate()

        self.procedure = [
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
                "text": "would you like to use the buddy randomizer? (you can change this later in config > buddy_randomizer)",
                "method": self.prompt_buddy_randomizer,
                "args": None,
            },
            {
                "text": "would you like to use the skin randomizer? (you can change this later in config > skin_randomizer)",
                "method": self.prompt_skin_randomizer,
                "args": None,
            },
            {
                "text": None,
                "method": self.check_prime_karambit,
                "args": None,
            }
        ]
        self.run()


    def run(self):

        for item in self.procedure:
            returned = None
            color_print([("Green", item["text"])]) if item["text"] is not None else print()
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

    def prompt_skin_randomizer(self):
        use_randomizer = inquirer.confirm("use skin randomizer?",default=True).execute()
        if use_randomizer:
            color_print([("Green","set up your randomizer pool using your ARROW KEYS and ENTER for navigation")])
            Randomizer_Editor.randomizer_entrypoint()
        else:
            self.config["skin_randomizer"]["enabled"] = False
            app_config.modify_config(self.config)
        
    def prompt_buddy_randomizer(self):
        use_randomizer = inquirer.confirm("use buddy randomizer?",default=True).execute()
        if not use_randomizer:
            self.config["buddy_randomizer"]["enabled"] = False
            app_config.modify_config(self.config)
        
    def check_prime_karambit(self):
        skins = Skin_Manager.fetch_skin_data()

        skin_uuid = "9237e734-4a2a-38ae-7438-6cbee901877d"
        upgraded_uuid = "a3c2dd26-4705-8e42-cce1-6bae0236ac7a"

        command = "set Melee Prime//2.0-Karambit Level-1"

        if skin_uuid in skins["2f59173c-4bed-b6c3-2191-dea9b58be9c7"]["skins"].keys():
            if upgraded_uuid in skins["2f59173c-4bed-b6c3-2191-dea9b58be9c7"]["skins"][skin_uuid]["levels"].keys():
                color_print([("Yellow bold","you have an upgraded prime karambit! would you like to equip and downgrade it?")])
                if inquirer.confirm("downgrade prime karambit?").execute():
                    Set_Skin(self.client,command.split(" "))
                    color_print([("Blue","\nrun "),("White",command),("Blue", " to downgrade it the next time you launch VALORANT")]) 
                    time.sleep(5)