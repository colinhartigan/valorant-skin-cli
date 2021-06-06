from termcolor import cprint

class Set_Title:
    def __init__(self,command,manager):

        if len(command) < 2:
            cprint("command missing required params", "red")
            return

        title_name = ' '.join(i for i in command[2:])
        title = manager.fetch_title_by_name(title_name)

        if title is not None:
            manager.modify_title(title['uuid'])

            cprint(f"Title -> {title['titleText']}", "green", attrs=["bold"])
