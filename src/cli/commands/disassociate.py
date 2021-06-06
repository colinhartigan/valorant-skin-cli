from termcolor import cprint 

class Disassociate:

    def __init__(self,match_manager):

        match_manager.refresh()
        match_id = match_manager.match_id

        if match_id is not None:
            print(match_manager.disassociate_player())
            cprint(f"successfully dodged match {match_id}","green",attrs=["bold"])
        else:
            cprint("not in game","red")