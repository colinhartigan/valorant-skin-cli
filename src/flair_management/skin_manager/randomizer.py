from termcolor import cprint
from ...content.skin_content import Skin_Content
from ...flair_loader.skin_loader import Loader
import random

class Randomize:

    def __init__(self,manager):
        loadout = manager.fetch_loadout()
        all_skins = Loader.fetch_skin_data()

        # this spawn of satan creates a streamlined dict of weapons enabled in the randomizer pool
        randomizer_pool = {weapon: {skin: {'display_name': skin_data['display_name'], 'levels': {level: level_data for level,level_data in skin_data['levels'].items() if level_data['enabled']}, 'chromas': {chroma: chroma_data for chroma,chroma_data in skin_data['chromas'].items() if chroma_data['enabled']}} for skin,skin_data in weapon_data['skins'].items() if skin_data['enabled']} for weapon,weapon_data in all_skins.items()}

        for weapon in loadout['Guns']:
            weapon_data = randomizer_pool[weapon['ID']]

            # if data is blank just leave skin as is
            if weapon_data != {}:
                random_index = random.randrange(0,len(weapon_data)) # pick a random skin from the set

                skin = weapon_data[list(weapon_data.keys())[random_index]] 

                level_index = random.randrange(0,len(skin['levels']))
                chroma_index = random.randrange(0,len(skin['chromas'])) if len(skin['chromas']) > 0 else 0
                
                weapon['SkinID'] = list(weapon_data.keys())[random_index]
                weapon['SkinLevelID'] = list(skin['levels'].keys())[level_index]
                weapon['ChromaID'] = list(skin['chromas'].keys())[chroma_index]
            
        new = manager.put_loadout(loadout=loadout)
        
        cprint("randomized skins", "green", attrs=["bold"])