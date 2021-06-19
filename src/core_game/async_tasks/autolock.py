from termcolor import cprint
import asyncio
import time

from ...content.coregame_content import Coregame_Content
from ...utility.config_manager import Config

class Autolocker:
    '''
    i̶n̶s̶t̶a̶l̶o̶c̶k̶e̶r̶  autolocker (this specifically is definitely not an instalocker and i definitely dont essentially get an advantage for using this, which particularly is fairly significant.)
    '''

    def __init__(self,client):
        self.client = client
        self.tic = 0
        self.toc = 0

    async def run(self):
        self.config = Config.fetch_config()
        if self.config["autolock"]["enabled"]:
            try:
                self.tic = time.perf_counter()
                if self.config["autolock"]["delay"] != 0:
                    cprint(f"autolock delay: {self.config['autolock']['delay']}s","cyan")
                await asyncio.sleep(self.config["autolock"]["delay"])
                agent = self.config["autolock"]["target"]
                agent_data = Coregame_Content.fetch_agent_by_name(agent)
                if agent_data is not None:
                    match_data = self.client.fetch_pregame_from_puuid()
                    match_id = match_data["MatchID"]
                    agent_id = agent_data["uuid"]
                    response = self.client.lock_character(match_id, agent_id)
                    self.toc = time.perf_counter()
                    cprint(f"autolocked as {agent_data['displayName']} in {self.toc-self.tic:0.2f}s (match_id: {match_id})","green",attrs=["bold"])
                else:
                    cprint(f"'{self.config['autolock']['target']}' is an invalid agent","red")
            except:
                cprint("unable to autolock","red")

        else:
            cprint("REMINDER: autolocker is disabled","cyan")