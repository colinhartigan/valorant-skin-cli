from termcolor import cprint

class Help:
    def __init__(self,command,help_data):
        try:
            cmd = command[1]
        except:
            cmd = "help"
        
        try:
            data = help_data[cmd]

            cprint(f"HELP FOR {cmd.upper()}","yellow",attrs=["bold"])
            cprint(f"description: {data['desc']}","cyan")

            if "params" in data.keys():
                cprint("PARAMETERS","yellow",attrs=["underline"])
                cprint("\n".join(f"{param} \t -> {desc}" for param,desc in data['params'].items()),"green")

            if "commands" in data.keys():
                cprint("COMMANDS","yellow",attrs=["underline"])
                cprint("\n".join(f"{param} \t -> {desc}".expandtabs(12) for param,desc in data['commands'].items()),"green")

            if "bottom" in data.keys():
                cprint(data['bottom'],"cyan")

        except Exception as e:
            print(e)