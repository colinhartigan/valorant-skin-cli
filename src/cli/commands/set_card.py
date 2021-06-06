from termcolor import cprint

class Set_Card:
    def __init__(self,command,manager):

        if len(command) < 2:
            cprint("command missing required params", "red")
            return

        card_name = ' '.join(i for i in command[1:])
        card = manager.fetch_card_by_name(card_name)

        if card is not None:
            manager.modify_card(card['uuid'])

            cprint(f"Card -> {card['displayName']}", "green", attrs=["bold"])
