from valclient.client import Client
import os 
import json
import random
import requests
from termcolor import colored, cprint

here = os.path.dirname(os.path.abspath(__file__))

client = Client()
client.hook()

class Manager:

    def fetch_loadout(self):
        return client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return client.put_player_loadout(loadout=loadout)

    def fetch_gun_pool(self):
        with open(os.path.join(here, 'gun_pool.json')) as f:
            gun_pool = json.load(f)
            return gun_pool

    def fetch_weapon_data(self,weapon_uuid,weapon_datas):
        for i in weapon_datas:
            if i['uuid'] == weapon_uuid:
                return i



    def modify_skin(self,weapon_uuid,skin_uuid,level_uuid,chroma_uuid):
        loadout = self.fetch_loadout()
        
        for weapon in loadout['Guns']:
            if weapon['ID'] == weapon_uuid:
                weapon['SkinID'] = skin_uuid 
                weapon['SkinLevelID'] = level_uuid 
                weapon['ChromaID'] = chroma_uuid     
                
        self.put_loadout(loadout=loadout)


    def randomize_skins(self):
        loadout = self.fetch_loadout()
        print(loadout)

        weapon_datas = requests.get(f"https://valorant-api.com/v1/weapons")
        weapon_datas = weapon_datas.json()['data']

        gun_pool = self.fetch_gun_pool()
        for i in loadout['Guns']:
            weapon_uuid = i['ID']

            weapon_data = self.fetch_weapon_data(weapon_uuid,weapon_datas)
            weapon_name = weapon_data['displayName']

            skins = gun_pool[weapon_uuid] # find valid skins by weapon uuid
            amount = len(skins) # determine how many skins there are for a weapon
            choice = list(skins)[random.randrange(0,amount)] # pick a random skin from the set
            skin = skins[choice] # get skin info
            
            level = list(skin['levels'])[random.randrange(0,len(skin['levels']))]
            chroma = list(skin['chromas'])[random.randrange(0,len(skin['chromas']))]

            print(f"{weapon_name}\t-> {choice}\t({level}/{chroma})")

            i['SkinID'] = skin['uuid']
            i['SkinLevelID'] = skin['levels'][level] 
            i['ChromaID'] = skin['chromas'][chroma]

        new = self.__put_loadout(loadout=loadout)
        print("ok" if loadout['Guns'] == new['Guns'] else "nope")

