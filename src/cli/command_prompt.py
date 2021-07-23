import os, ctypes
from InquirerPy import inquirer 

from ..flair_management.skin_manager.randomizer_editor import Editor

from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..flair_management.skin_manager.randomizer import Randomizer
from ..flair_loader.skin_loader_withcheck import Loader

from ..core_game.session import Session

# command imports
from .completer_generator import Completer
from .validator import Command_Validator
from .commands import (loadout, set_skin, config, reload, reset, test)

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128) #disable inputs to console


class Prompt:

    def __init__(self, auth_data=None, client=None):
        self.client = client

        self.skin_data = Loader.fetch_skin_data()

        self.commands = Completer.generate_completer_dict()

    def main_loop(self):
        command = [""]

        while command[0] != "exit":

            command = inquirer.text(
                message=">",
                qmark="",
                completer=self.commands,
                validate=Command_Validator(),
                #transformer=lambda result: result.replace("-", " "),
                filter=lambda result: [i.strip() for i in result.split()],
                multicolumn_complete=True,
                invalid_message="invalid command"
            ).execute()

            if command[0] == "randomize":
                Randomizer.randomize(self.client)
                loadout.Loadout(self.client)

            if command[0] == "modify":
                Editor.select_weapon_type(None)

            if command[0] == "set":
                set_skin.Set_Skin(self.client, command, self.skin_data)

            if command[0] == "loadout":
                loadout.Loadout(self.client)

            if command[0] == "test":
                test.Test(self.client)


            if command[0] == "reset":
                reset.Reset()

            if command[0] == "config":
                config.Config_Editor()

            if command[0] == "reload": 
                reload.Reload()
                os._exit(1)

        os._exit(1)