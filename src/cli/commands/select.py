from termcolor import cprint
import time

class Select:

    def __init__(self,command,session,client):

        if len(command) < 2:
            cprint("command missing required params", "red")
            return

        agent_name = command[1]
        agent_data = session.fetch_agent_by_name(agent_name)

        if agent_data is not None:
            try:
                match_data = client.fetch_pregame_from_puuid()
                match_id = match_data["MatchID"]
                client.select_character(match_id,agent_data['uuid'])

                cprint(f"selected {agent_data['displayName']}","green",attrs=["bold"])
            except:
                cprint(f"not in a match","red")