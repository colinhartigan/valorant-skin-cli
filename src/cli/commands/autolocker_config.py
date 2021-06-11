from termcolor import cprint

class Autolocker_Config:

    def __init__(self,command,config,session):

        if len(command) < 2:
            cprint("command missing required params", "red")
            return

        if command[1] == "enable" or command[1] == "disable":
            new_config = config.fetch_config()
            new_config["autolock"]["enabled"] = True if command[1] == "enable" else False
            config.modify_config(new_config)

            cprint(f"autolocker {''.join('enabled' if command[1] == 'enable' else 'disabled')}","green",attrs=["bold"])

        elif command[1] == "set":
            agent_name = command[2]
            agent_data = session.fetch_agent_by_name(agent_name)

            if agent_data is not None:
                new_config = config.fetch_config()
                new_config["autolock"]["target"] = agent_data['displayName']
                config.modify_config(new_config)
                cprint(f"autolock target set to {agent_data['displayName']}","green",attrs=["bold"])

            else:
                cprint("invalid agent","red")

        elif command[1] == "delay":
            time = int(command[2])
            if isinstance(time,int):
                new_config = config.fetch_config()
                new_config["autolock"]["delay"] = time 
                config.modify_config(new_config)

                cprint(f"autolock delay set to {time}","green",attrs=["bold"])

            else:
                cprint("invalid time (needs to be int)", "red")

        else:
            cprint("invalid arguments","red")