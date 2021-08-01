from ...utility.filepath import Filepath
from ...content.skin_content import Skin_Content
import os,json

class Skin_Manager:

    @staticmethod
    def modify_skin(client,weapon_uuid,skin_uuid,level_uuid,chroma_uuid):
        loadout = client.fetch_player_loadout()
        
        for weapon in loadout['Guns']:
            if weapon['ID'] == weapon_uuid:
                weapon['SkinID'] = skin_uuid 
                weapon['SkinLevelID'] = level_uuid 
                weapon['ChromaID'] = chroma_uuid     
                
        client.put_player_loadout(loadout=loadout)

    @staticmethod
    def modify_skin_data(new_data):
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'skins.json')), 'w') as f:
            json.dump(new_data, f)

    @staticmethod
    def fetch_skin_data():
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'skins.json'))) as f:
            return json.load(f)

    @staticmethod
    def generate_blank_skin_file():
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'skins.json')), 'w') as f:
            new_data = {}

            all_weapon_content = Skin_Content.fetch_weapons_data()
            for weapon in all_weapon_content:
                weapon_uuid = weapon["uuid"]
                weapon_data = {
                    "display_name": weapon["displayName"],
                    "skins": {}
                }

                new_data[weapon_uuid] = weapon_data

            json.dump(new_data, f)