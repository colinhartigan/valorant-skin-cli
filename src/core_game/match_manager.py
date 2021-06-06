from termcolor import cprint

class Match_Manager:

    def __init__(self,client):
        self.client = client
        self.match_id = ""

    def refresh(self):
        data = self.client.coregame_fetch_player()
        self.match_id = self.client.coregame_fetch_player()["MatchID"] if data is not None else None

    def disassociate_player(self):
        return self.client.coregame_disassociate_player(self.match_id)