import asyncio

from .async_tasks.randomize import Randomizer
from .async_tasks.instalock import Instalocker

class Session:
    '''
    this one's in charge of activating session-related tasks such as instalocking, skin randomizing after match, etc.
    '''

    def __init__(self,client,manager):
        self.client = client 
        self.skin_manager = manager

        self.previous_presence = self.client.fetch_presence()
        self.presence = self.previous_presence

    async def randomizer_check(self):
        if (self.presence["sessionLoopState"] != self.previous_presence["sessionLoopState"]) and (self.previous_presence["sessionLoopState"] == "INGAME" and self.presence["sessionLoopState"] == "MENUS"):
            Randomizer(self.skin_manager)

    async def instalocker_check(self):
        if (self.presence["sessionLoopState"] != self.previous_presence["sessionLoopState"]) and (self.previous_presence["sessionLoopState"] == "MENUS" and self.presence["sessionLoopState"] == "PREGAME"):
            Instalocker(self.client)

    async def update_presence(self):
        self.previous_presence = self.presence 

        presence = self.client.fetch_presence()
        self.presence = presence
        await self.randomizer_check()

        return self.presence