from InquirerPy.utils import color_print
from InquirerPy import inquirer 

from ..skin_manager.skin_manager import Skin_Manager
from ...cli.commands.loadout import Loadout

class Loadout_Creator:

    @staticmethod
    def create_loadout(client):
        color_print([("Blue bold","\nLOADOUT CREATOR --------------------")])
        equipped_loadout = client.fetch_player_loadout()

        loadout_name = inquirer.text(
            message="name this loadout:",
            validate=lambda response: isinstance(response, str)
        ).execute()

        color_print([("Blue bold", "\npreview your loadout")])
        Loadout(client)

        confirm = inquirer.confirm(message=f"do you want to save this loadout as '{loadout_name}'?", default=True).execute()
        if confirm:
            print(equipped_loadout)