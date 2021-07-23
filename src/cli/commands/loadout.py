from InquirerPy.utils import color_print

from ...flair_management.skin_manager.skin_manager import Skin_Manager

class Loadout:

    def __init__(self):
        table = Skin_Manager.fetch_skin_table()
        print()
        for row in table:
            color_print([weapon for weapon in row])