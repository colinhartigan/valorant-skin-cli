from ...content.title_content import Title_Content

class Title_Manager:
    def __init__(self,client=None):
        self.client = client

    def fetch_loadout(self):
        return self.client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return self.client.put_player_loadout(loadout=loadout)

    def fetch_all_titles(self):
        return Title_Content.fetch_all_titles()

    def fetch_title_by_name(self,title_name):
        return Title_Content.fetch_title_by_name(title_name)


    def modify_title(self,title_uuid):
        loadout = self.fetch_loadout() 

        loadout['PlayerTitle']['ID'] = title_uuid 
        loadout['Identity']['PlayerTitleID'] = title_uuid

        self.put_loadout(loadout)