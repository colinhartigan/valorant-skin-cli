from InquirerPy.utils import color_print

class Loadout:

    def __init__(self,manager):
        table = manager.fetch_skin_table()
        print()
        for row in table:
            color_print([weapon for weapon in row])