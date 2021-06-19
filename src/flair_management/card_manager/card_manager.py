from ...content.card_content import Card_Content

class Card_Manager:
    def __init__(self,client=None):
        self.client = client

    def fetch_loadout(self):
        return self.client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return self.client.put_player_loadout(loadout=loadout)

    def fetch_all_cards(self):
        return Card_Content.fetch_all_titles()

    def fetch_card_by_name(self,title_name):
        return Card_Content.fetch_card_by_name(title_name)

    def modify_card(self,title_uuid):
        loadout = self.fetch_loadout() 

        loadout['PlayerCard']['ID'] = title_uuid 
        loadout['Identity']['PlayerCardID'] = title_uuid

        self.put_loadout(loadout)