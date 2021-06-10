from termcolor import cprint

class Test:

    def __init__(self,client):
        self.client = client
        loadout = self.client.fetch_player_loadout()
        print(loadout)
        for spray in loadout["Sprays"]:
            spray["SprayID"] = "a78eb46a-4d66-4683-9a77-02adae482146"
        self.client.put_player_loadout(loadout=loadout)
        cprint("ok","green",attrs=["bold"])