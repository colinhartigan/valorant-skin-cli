from InquirerPy.utils import color_print
import os

from ...flair_management.loadout_grid import Loadout_Grid

class Loadout:

    def __init__(self,client):
        table, width = Loadout_Grid.fetch_loadout_grid(client)
        #os.system(f"mode con: cols={width} lines=30")
        print()
        for row in table:
            color_print([weapon for weapon in row])