from termcolor import cprint
import time

class Lock:

    def __init__(self,command,session,client):

        self.tic = time.perf_counter()

        if len(command) < 2:
            cprint("command missing required params", "red")
            return

        agent_name = command[1]
        agent_data = session.fetch_agent_by_name(agent_name)

        if agent_data is not None:
            try:
                match_data = client.fetch_pregame_from_puuid()
                match_id = match_data["MatchID"]
                client.lock_character(match_id,agent_data['uuid'])
                self.toc = time.perf_counter() 

                cprint(f"locked in as {agent_data['displayName']} in {self.toc-self.tic:0.2f}s","green",attrs=["bold"])
            except:
                cprint(f"not in a match","red")