import asyncio

class Session:
    '''
    this one's in charge of activating session-related tasks such as instalocking, skin randomizing after match, etc.
    '''

    def __init__(self,client,manager):
        self.client = client 
        self.skin_manager = manager

        self.previous_presence = self.client.fetch_presence()
        self.presence = self.previous_presence

    def fetch_loop_state(self):
        return self.presence["sessionLoopState"]

    def randomizer_check(self,presence):
        if (presence["sessionLoopState"] != self.previous_presence["sessionLoopState"]) and (self.previous_presence["sessionLoopState"] == "INGAME" and presence["sessionLoopState"] == "MENUS"):
            self.skin_manager.randomize_skins()

    async def update(self):
        self.previous_presence = self.presence 

        presence = self.client.fetch_presence()
        self.presence = presence
        self.randomizer_check(presence)

        return self.presence    