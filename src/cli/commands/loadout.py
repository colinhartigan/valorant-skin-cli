from InquirerPy.utils import color_print
import os

from ...flair_management.loadout_manager.loadout_actions import Loadout_Actions
from ...flair_management.loadout_manager.loadouts_manager import Loadouts_Manager 
from ...flair_management.loadout_grid import Loadout_Grid


class Loadout:
    def __init__(self,command,client):
        if len(command) == 1:
            table, width = Loadout_Grid.fetch_loadout_grid(client)
            print()
            for row in table:
                color_print([weapon for weapon in row])
        else:
            if command[1] == "create": 
                Loadout_Actions.create_loadout(client)

            if len(command) == 3:
                if command[1] == "equip": 
                    Loadout_Actions.equip_loadout(command[2].replace("-"," "), client)

                if command[1] == "preview":
                    loadout = Loadouts_Manager.fetch_loadout_by_name(command[2].replace("-"," "))
                    Loadout_Actions.print_loadout(client,loadout)

                if command[1] == "delete":
                    Loadout_Actions.delete_loadout(command[2].replace("-"," "))
            else:
                color_print([("Red","command missing required params")])