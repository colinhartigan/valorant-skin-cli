
from termcolor import colored, cprint
import sys
import os
from InquirerPy import prompt,inquirer
from InquirerPy.separator import Separator

from ..utility.config_manager import Config

from ..flair_loader.skin_editor import Editor

from ..flair_management.skin_manager.skin_manager import Skin_Manager

from ..core_game.session import Session

#command imports 
from .commands.autolocker_config import Autolocker_Config
from .commands.select import Select
from .commands.lock import Lock
from .commands.set_skin import Set_Skin
from .commands.help import Help
from .commands.loadout import Loadout
from .commands.test import Test

class Prompt: 

    def __init__(self,auth_data=None,client=None):
        self.client = client

        self.skin_manager = Skin_Manager(client)
        self.gun_pool = self.skin_manager.fetch_gun_pool()

        self.session = Session(client,self.skin_manager)

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
                else:
                    print()
                listener = input()
                

            while listener == "":
                command = input("> ").split()
                if command == []:
                    command = [""]
                    listener = "success"

                if command[0] == "help":
                    Help(command,self.help_data)
                    listener = "success"

                if command[0] == "select" or command[0] == "sel":
                    Select(command,self.session,self.client)
                    listener = "success"

                if command[0] == "lock":
                    Lock(command,self.session,self.client)
                    listener = "success"

                if command[0] == "autolock":
                    Autolocker_Config(command,Config,Session)
                    listener = "success"

                if command[0] == "loadout":
                    Loadout(self.skin_manager)
                    listener = "success"

                if command[0] == "modify":
                    Editor.select_weapon()
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