from valclient.client import Client
import os 
import json
import random
import requests
here = os.path.dirname(os.path.abspath(__file__))

client = Client()
client.hook()

class skin_manager:
    @staticmethod
    def get_weapon_data(uuid,weapon_datas):
        for i in weapon_datas:
            if i['uuid'] == uuid:
                return i

    @staticmethod
    def randomize_skins():
        loadout = client.fetch_player_loadout()

        weapon_datas = requests.get(f"https://valorant-api.com/v1/weapons")
        weapon_datas = weapon_datas.json()['data']

        with open(os.path.join(here, 'gun_pool.json')) as f:
            gun_pool = json.load(f)
            for i in loadout['Guns']:
                weapon_uuid = i['ID']

                weapon_data = skin_manager.get_weapon_data(weapon_uuid,weapon_datas)
                weapon_name = weapon_data['displayName']

                skins = gun_pool[weapon_uuid] # find valid skins by weapon uuid
                amount = len(skins) # determine how many skins there are for a weapon
                choice = list(skins)[random.randrange(0,amount)] # pick a random skin from the set
                skin = skins[choice] # get skin info
                
                level = list(skin['levels'])[random.randrange(0,len(skin['levels']))]
                chroma = list(skin['chromas'])[random.randrange(0,len(skin['chromas']))]

                print(f"{weapon_name} -> {choice}\t({level}/{chroma})")

                i['SkinID'] = skin['uuid']
                i['SkinLevelID'] = skin['levels'][level] 
                i['ChromaID'] = skin['chromas'][chroma]

        new = client.put_player_loadout(loadout=loadout)
        print("ok" if loadout['Guns'] == new['Guns'] else "nope")

skin_manager.randomize_skins()