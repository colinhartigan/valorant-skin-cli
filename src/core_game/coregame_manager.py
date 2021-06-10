'''
async manager calls to coregame to update session
session keeps track of inmatch/map/other data about live match
'''
import asyncio 

from .session import Session

class Coregame_Manager:

    def __init__(self,client):
        self.client = client
        self.session = Session(self.client)

    async def main_loop(self):
        await self.session.update()

    def fetch_session(self):
        return self.session