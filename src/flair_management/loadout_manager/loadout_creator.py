from InquirerPy.utils import color_print
from InquirerPy import inquirer 

from ..skin_manager.skin_manager import Skin_Manager
from ...cli.commands.loadout import Loadout

class Loadout_Creator:

    @staticmethod
    def create_loadout(client):
        color_print([("Blue","\nLOADOUT CREATOR --------------------")])
        equipped_loadout = client.fetch_player_loadout()

        loadout_name = inquirer.text(
            message="name this loadout:",
            validate=lambda response: isinstance(response, str)
        ).execute()

        color_print([("White", "preview your loadout")])
        Loadout(client)