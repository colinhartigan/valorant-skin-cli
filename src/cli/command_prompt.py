
from termcolor import colored, cprint
import sys
import os

from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..flair_management.skin_manager.skin_loader import Loader

from ..flair_management.title_manager.title_manager import Title_Manager
from ..flair_management.card_manager.card_manager import Card_Manager

from ..core_game.session import Session

#command imports 
from .commands.set_skin import Set_Skin
from .commands.set_title import Set_Title
from .commands.set_card import Set_Card
from .commands.help import Help
from .commands.loadout import Loadout
from .commands.test import Test

class Prompt: 

    def __init__(self,auth_data=None,client=None):
        self.client = client

        self.skin_manager = Skin_Manager(client)
        self.gun_pool = self.skin_manager.fetch_gun_pool()

        self.title_manager = Title_Manager(client)
        self.card_manager = Card_Manager(client)

        #self.session = Session(client)

        # configuration stuffs
        self.auto_randomize = False

        self.help_data = {
            "set":{
                "desc":"set a gun's skin/level/chroma",
                "params":{
                    "[weapon_name]":"weapon's name (knife = melee)",
                    "[skin_name]":"skinline's name (reaver, prime)",
                    "(level_name)":"skin's upgrade level (defaults to 1)",
                    "(chroma_name)":"skin's chroma level (ex. 'blue', 'red'; defaults to Base)"
                },
                "bottom":"example: 'set vandal reaver 4 white'"
            },
            "help":{
                "desc":"overview of all commands",
                "commands":{
                    "help":"get this menu",
                    "set":"set a weapon's skin",
                    "randomize":"randomize each weapon's skin from the gun pool",
                    "loadout":"get the active skin loadout"
                },
                "bottom":"run 'setup' to set up your skin collection"
            },
            "loadout":{
                "desc":"get the active skin loadout",
            },
            "randomize":{
                "desc":"randomize your equipped skins",
            }
        }


    def main_loop(self):
        command = [""]
        cprint("VALORANT CLI - type 'help' for help",attrs=["bold","underline"])
        
        listener = "nope"

        while command[0] != "exit":
            while listener != "":
                if listener != "success":
                    cprint("press enter to type a command","yellow",attrs=["bold"])
                listener = input()
                

            while listener == "":
                command = input("> ").split()
                if command == []:
                    command = [""]

                if command[0] == "help":
                    Help(command,self.help_data)
                    listener = "success"

                if command[0] == "title":
                    Set_Title(command,self.title_manager)
                    listener = "success"

                if command[0] == "card":
                    Set_Card(command,self.card_manager)
                    listener = "success"

                if command[0] == "loadout":
                    Loadout(self.skin_manager)
                    listener = "success"

                if command[0] == "setup":
                    Loader.generate_skin_list()
                    Loader.generate_skin_datas()
                    listener = "success"

                if command[0] == "modify":
                    Loader.generate_skin_datas()
                    listener = "success"

                if command[0] == "set":
                    Set_Skin(command,self.skin_manager,self.gun_pool)
                    listener = "success"
                
                if command[0] == "randomize":
                    self.skin_manager.randomize_skins() 
                    Loadout(self.skin_manager)
                    listener = "success"

                if command[0] == "exit":
                    listener = "done"

                if command[0] == "test":
                    Test(self.client)
                    listener = "success"

        sys.exit()