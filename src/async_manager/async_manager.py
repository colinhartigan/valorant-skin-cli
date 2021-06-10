from termcolor import cprint
import asyncio
from time import sleep

from ..core_game.coregame_manager import Coregame_Manager

class Async_Manager:

    def __init__(self,client):
        self.loop = asyncio.get_event_loop()

        self.client = client 
        self.coregame_manager = Coregame_Manager(self.client)

    def init_loop(self):
        self.loop.run_until_complete(self.main_loop())

    async def main_loop(self):
        while True:
            # NONE OF THE CHILD MODULES SHOULD HAVE THEIR OWN LOOPS
            await self.coregame_manager.main_loop() # coregame loop

            await asyncio.sleep(5)