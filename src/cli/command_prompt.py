import os, ctypes
from InquirerPy import inquirer 

from ..flair_management.skin_manager.randomizer_editor import Randomizer_Editor
from ..flair_management.skin_manager.weight_editor import Weight_Editor

from ..flair_management.skin_manager.randomizer import Skin_Randomizer
from ..flair_management.gunbuddy_manager.randomizer import Buddy_Randomizer

# command imports
from .completer_generator import Completer
from .validator import Command_Validator
from .commands import (loadout, set_skin, config, reload, reset, randomize)

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128) #disable inputs to console


class Prompt:

    def __init__(self, auth_data=None, client=None, app_config=None):
        self.client = client
        self.commands = {}
        self.app_config = app_config
        Completer.cli = self
        Completer.generate_completer_dict()

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
                randomize.Randomize(command,self.client,self.app_config)

            if command[0] == "modify":
                Randomizer_Editor.randomizer_entrypoint()

            if command[0] == "weights":
                Weight_Editor.weights_entrypoint()

            if command[0] == "set":
                set_skin.Set_Skin(self.client, command)

            if command[0] == "loadout":
                loadout.Loadout(command, self.client)

            if command[0] == "reset":
                reset.Reset()

            if command[0] == "config":
                config.Config_Editor()

            if command[0] == "reload": 
                reload.Reload()
                os._exit(1)

            Completer.generate_completer_dict()

        os._exit(1)