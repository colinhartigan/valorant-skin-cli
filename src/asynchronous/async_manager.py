from InquirerPy.utils import color_print
import asyncio

from ..utility.config_manager import Config
from ..core_game.coregame_manager import Coregame_Manager

class Async_Manager:

    def __init__(self,client):
        self.loop = asyncio.get_event_loop()

        self.config = Config.fetch_config()
        self.client = client 
        self.coregame_manager = Coregame_Manager(self.client)

    def init_loop(self):
        color_print([("LimeGreen","async thread running!")])
        self.loop.run_until_complete(self.main_loop())

    async def main_loop(self):
        '''
        for refreshing non-time-essential async tasks
        '''
        while True:
            # NONE OF THE CHILD MODULES SHOULD HAVE THEIR OWN LOOPS
            await self.coregame_manager.main_loop() # coregame loop

            await asyncio.sleep(self.config["async_refresh_interval"])