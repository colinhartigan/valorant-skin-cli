import os, sys
from InquirerPy.utils import color_print

from .async_tasks.randomize import Randomizer

class Session:
    '''
    this one's in charge of activating session-related tasks
    '''

    def __init__(self,client):
        self.client = client 

        try:
            self.previous_presence = self.client.fetch_presence()
        except:
            self.previous_presence = {}
        self.presence = self.previous_presence
        self.ingame = False

    async def randomizer_check(self):
        if self.presence is not None:
            if (self.presence["sessionLoopState"] != self.previous_presence["sessionLoopState"]) and (self.previous_presence["sessionLoopState"] == "INGAME" and self.presence["sessionLoopState"] == "MENUS"):
                color_print([("Cyan bold","-- GG --")])
                Randomizer(self.client)
        else:
            os._exit(1)
        
    async def update_presence(self):
        self.previous_presence = self.presence 

        try:
            self.presence = self.client.fetch_presence()
        except:
            os._exit(1)
        await self.randomizer_check()            

        return self.presence