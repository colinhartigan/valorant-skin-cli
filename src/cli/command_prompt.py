
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
from .completer_generator import Completer
from .commands import (loadout)

class Prompt: 

    def __init__(self,auth_data=None,client=None):
        self.client = client

        self.skin_manager = Skin_Manager(client)
        self.gun_pool = self.skin_manager.fetch_gun_pool()

        self.session = Session(client,self.skin_manager)

        # configuration stuffs
        self.auto_randomize = False

        self.commands = Completer.generate_completer_dict()

    def main_loop(self):
        command = ""

        while command != "exit":
            command = inquirer.text(
                message="",
                qmark=">",
                completer=self.commands,
                validate=lambda result: result.split()[0].strip() in list(self.commands.keys()),
                transformer=lambda result: result.split()[0].strip(),
                filter = lambda result: result.strip(),
                multicolumn_complete=True,
            ).execute()

            if command == "randomize":
                self.skin_manager.randomize_skins()
                loadout.Loadout(self.skin_manager)

            if command == "modify":
                Editor.select_weapon()
            



'''
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
'''