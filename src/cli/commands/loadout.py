from InquirerPy.utils import color_print

class Loadout:

    def __init__(self,manager):
        table, longest = manager.fetch_skin_table()
        color_print([("LimeGreen",table.expandtabs(longest+3))])