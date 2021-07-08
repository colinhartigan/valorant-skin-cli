import sys
from InquirerPy import prompt, inquirer
from InquirerPy.separator import Separator

from ..utility.config_manager import Config

from ..flair_management.skin_manager.randomizer_editor import Editor

from ..flair_management.skin_manager.skin_manager import Skin_Manager

from ..core_game.session import Session

# command imports
from .completer_generator import Completer
from .validator import Command_Validator
from .commands import (loadout, set_skin, config)


class Prompt:

    def __init__(self, auth_data=None, client=None):
        self.client = client

        self.skin_manager = Skin_Manager(client)
        self.skin_data = self.skin_manager.fetch_inventory_data()

        self.session = Session(client, self.skin_manager)

        self.commands = Completer.generate_completer_dict()

    def main_loop(self):
        command = ""

        while command != "exit":

            command = inquirer.text(
                message=">",
                qmark="",
                completer=self.commands,
                validate=Command_Validator(),
                transformer=lambda result: result.replace("-", " "),
                filter=lambda result: [i.strip() for i in result.split()],
                multicolumn_complete=True,
                invalid_message="invalid command"
            ).execute()

            if command[0] == "randomize":
                self.skin_manager.randomize_skins()
                loadout.Loadout(self.skin_manager)

            if command[0] == "modify":
                Editor.select_weapon_type()

            if command[0] == "set":
                set_skin.Set_Skin(command, self.skin_manager, self.skin_data)

            if command[0] == "loadout":
                loadout.Loadout(self.skin_manager)

            if command[0] == "config":
                config.Config_Editor()

        sys.exit()
