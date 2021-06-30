from termcolor import cprint

class Loadout:

    def __init__(self,manager):
        table, longest = manager.fetch_skin_table()
        cprint(table.expandtabs(longest+3),"green")