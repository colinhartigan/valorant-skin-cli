import os 
import json

from ...utility.config_manager import Config
from ...content.skin_content import Skin_Content
#from .skin_loader import Loader
from .randomizer import Randomize

class Skin_Manager:

    def __init__(self,client=None):
        self.client = client

    def fetch_loadout(self):
        return self.client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return self.client.put_player_loadout(loadout=loadout)

    @staticmethod
    def fetch_inventory_data():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data', 'skin_data.json'))) as f:
            gun_pool = json.load(f)
            return gun_pool

    @staticmethod
    def fetch_weapon_data(weapon_uuid,weapon_datas):
        for i in weapon_datas:
            if i['uuid'] == weapon_uuid:
                return i

    @staticmethod
    def fetch_skin_data(skin_uuid,skin_datas):
        for i in skin_datas:
            if i['uuid'] == skin_uuid:
                return i

    @staticmethod
    def fetch_max_level_for_skin(gun_pool,weapon_uuid,skin_uuid):
        for gun,data in gun_pool.items():
            if gun == weapon_uuid:
                for skin,skin_data in data.items():
                    if skin_data["uuid"] == skin_uuid:
                        return list(skin_data["levels"].items())[-1][0],list(skin_data["levels"].items())[-1][1]

    @staticmethod
    def fetch_default_chroma_for_skin(gun_pool,weapon_uuid,skin_uuid):
        for gun,data in gun_pool.items():
            if gun == weapon_uuid:
                for skin,skin_data in data.items():
                    if skin_data["uuid"] == skin_uuid:
                        return list(skin_data["chromas"].items())[0][0],list(skin_data["chromas"].items())[0][1]

    @staticmethod
    def fetch_weapon_by_name(name):
        return Skin_Content.fetch_weapon_by_name(name)

    def fetch_skin_table(self):

        loadout = self.fetch_loadout()['Guns']
        skins = {}
        grid = {}

        longest = 0

        weapons_datas = Skin_Content.fetch_weapon_datas()
        skins_datas = Skin_Content.fetch_skin_datas()

        for skin in loadout:
            skin_data = self.fetch_skin_data(skin['SkinID'],skins_datas)
            weapon_data = self.fetch_weapon_data(skin['ID'],weapons_datas)

            grid[weapon_data['displayName']] = skin_data['displayName']
            if len(skin_data['displayName']) > longest:
                longest = len(skin_data['displayName'])

        # if only the api would return the guns in the right order :(
        return f"{grid['Classic']}\t{grid['Stinger']}\t{grid['Bulldog']}\t{grid['Marshal']}\n{grid['Shorty']}\t{grid['Spectre']}\t{grid['Guardian']}\t{grid['Operator']}\n{grid['Frenzy']}\t{grid['Bucky']}\t{grid['Phantom']}\t{grid['Ares']}\n{grid['Ghost']}\t{grid['Judge']}\t{grid['Vandal']}\t{grid['Odin']}\n{grid['Sheriff']}\t\t\t{grid['Melee']}", longest



    def modify_skin(self,weapon_uuid,skin_uuid,level_uuid,chroma_uuid):
        loadout = self.fetch_loadout()
        
        for weapon in loadout['Guns']:
            if weapon['ID'] == weapon_uuid:
                weapon['SkinID'] = skin_uuid 
                weapon['SkinLevelID'] = level_uuid 
                weapon['ChromaID'] = chroma_uuid     
                
        self.put_loadout(loadout=loadout)


    def randomize_skins(self):
        Randomize(self)
        