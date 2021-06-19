from termcolor import cprint
from ...content.skin_content import Skin_Content
import random

class Randomize:

    def __init__(self,manager):
        cprint("randomized skins", "green", attrs=["bold"])
        loadout = manager.fetch_loadout()

        weapon_datas = Skin_Content.fetch_weapon_datas()

        gun_pool = manager.fetch_gun_pool()
        for i in loadout['Guns']:
            weapon_uuid = i['ID']

            weapon_data = manager.fetch_weapon_data(weapon_uuid,weapon_datas)
            weapon_name = weapon_data['displayName']

            skins = gun_pool[weapon_uuid] # find valid skins by weapon uuid
            amount = len(skins) # determine how many skins there are for a weapon
            if amount != 0:
                choice = list(skins)[random.randrange(0,amount)] # pick a random skin from the set
                skin = skins[choice] # get skin info
                
                level = list(skin['levels'])[random.randrange(0,len(skin['levels']))]
                chroma = list(skin['chromas'])[random.randrange(0,len(skin['chromas']))]

                i['SkinID'] = skin['uuid']
                i['SkinLevelID'] = skin['levels'][level] 
                i['ChromaID'] = skin['chromas'][chroma]

        new = manager.put_loadout(loadout=loadout)