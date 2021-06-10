import requests

class Coregame_Content:
    
    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod
    def fetch_agent_datas():
        agents = Coregame_Content.fetch(endpoint="/agents")

    def fetch_agent_by_name(name):
        agents = Coregame_Content.fetch(endpoint="/agents")["data"]

        for agent in agents:
            if name.lower() in agent['displayName'].lower():
                return agent
        return None