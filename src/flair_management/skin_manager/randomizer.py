from InquirerPy.utils import color_print
from .skin_manager import Skin_Manager
from ...utility.config_manager import Config
import random

class Skin_Randomizer:

    config = Config.fetch_config()

    @staticmethod
    def randomize(client):
        loadout = client.fetch_player_loadout()
        equipped_skin_ids = [weapon['SkinID'] for weapon in loadout['Guns']]
        all_skins = Skin_Manager.fetch_skin_data()

        # this spawn of satan creates a streamlined dict of weapons enabled in the randomizer pool
        randomizer_pool = {weapon: {skin: {'weight': skin_data['weight'], 'levels': {level: level_data for level,level_data in skin_data['levels'].items() if level_data['enabled']}, 'chromas': {chroma: chroma_data for chroma,chroma_data in skin_data['chromas'].items() if chroma_data['enabled']}} for skin,skin_data in weapon_data['skins'].items() if skin_data['enabled']} for weapon,weapon_data in all_skins.items()}
        randomizer_pool_no_repeats = {weapon: {skin: skin_data for skin,skin_data in weapon_data.items() if not skin in equipped_skin_ids} for weapon,weapon_data in randomizer_pool.items()}

        for weapon in loadout['Guns']:
            weapon_data = randomizer_pool_no_repeats[weapon['ID']] if (Skin_Randomizer.config["skin_randomizer"]["prevent_repeats"] and len(randomizer_pool_no_repeats[weapon['ID']]) > 1) else randomizer_pool[weapon['ID']]

            # if data is blank just leave skin as is
            if weapon_data != {}:
                weights = (weapon_data[skin]['weight'] for skin in weapon_data)
                
                skin_uuid = random.choices(list(weapon_data.keys()), weights=weights)[0]
                skin = weapon_data[skin_uuid]

                level_index = random.randrange(0,len(skin['levels']))
                chroma_index = random.randrange(0,len(skin['chromas'])) if len(skin['chromas']) > 0 else 0
                
                weapon['SkinID'] = skin_uuid
                weapon['SkinLevelID'] = list(skin['levels'].keys())[level_index]
                weapon['ChromaID'] = list(skin['chromas'].keys())[chroma_index]
            else:
                color_print([("Yellow bold", f"[!] {all_skins[weapon['ID']]['display_name']} has no skins in the randomizer pool, using currently equipped skin")])
            
        new = client.put_player_loadout(loadout=loadout)
        
        color_print([("Lime", "randomized skins")])