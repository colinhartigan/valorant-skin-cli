from termcolor import cprint

from ..coregame_content import Coregame_Content
from ...utility.config_manager import Config

class Instalocker:
    '''
    i̶n̶s̶t̶a̶l̶o̶c̶k̶e̶r̶  this is definitely an autolocker, not an instalocker
    '''

    def __init__(self,client):
        self.client = client
        self.config = Config.fetch_config()

        if self.config["instalock"]["enabled"]:

            agent = self.config["instalock"]["target"]
            agent_data = Coregame_Content.fetch_agent_by_name(agent)
            if agent_data is not None:
                match_data = self.client.fetch_pregame_from_puuid()
                
                match_id = match_data["MatchID"]
                agent_id = agent_data["uuid"]

                self.client.lock_character(match_id, agent_id)
                cprint(f"locked in {agent_data['displayName']} (match_id: {match_id})","green",attrs=["bold"])
            else:
                cprint(f"'{self.config['instalock']['target']}' is an invalid agent","red")