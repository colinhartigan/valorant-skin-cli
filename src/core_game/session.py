import asyncio
import sys
from termcolor import cprint

from .async_tasks.randomize import Randomizer

from ..content.coregame_content import Coregame_Content

class Session:
    '''
    this one's in charge of activating session-related tasks
    '''

    def __init__(self,client,manager):
        self.client = client 
        self.skin_manager = manager

        try:
            self.previous_presence = self.client.fetch_presence()
        except:
            self.previous_presence = {}
        self.presence = self.previous_presence
        self.ingame = False

    @staticmethod
    def fetch_agent_by_name(name):
        return Coregame_Content.fetch_agent_by_name(name)

    async def randomizer_check(self):
        try:
            if (self.presence["sessionLoopState"] != self.previous_presence["sessionLoopState"]) and (self.previous_presence["sessionLoopState"] == "INGAME" and self.presence["sessionLoopState"] == "MENUS"):
                Randomizer(self.skin_manager)
        except:
            cprint("VALORANT is no longer running, terminating thread!","red")
            sys.exit()


    async def update_presence(self):
        self.previous_presence = self.presence 

        self.presence = self.client.fetch_presence()

        await self.randomizer_check()

        return self.presence