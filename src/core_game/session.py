import asyncio

class Session:

    def __init__(self,client):
        self.client = client 
        self.presence = {
            
        }

    async def update(self):
        presence = self.client.fetch_presence()
        self.presence = presence

    def fetch_loop_state(self):
        return self.presence["sessionLoopState"]