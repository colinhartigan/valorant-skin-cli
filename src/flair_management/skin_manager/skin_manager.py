import os, json
from InquirerPy.utils import color_print

from ...content.skin_content import Skin_Content
from ...utility.filepath import Filepath
from ...flair_loader.skin_loader_withcheck import Loader
from .randomizer import Randomize

class Skin_Manager:

    def __init__(self,client=None):
        self.client = client

    def fetch_loadout(self):
        return self.client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return self.client.put_player_loadout(loadout=loadout)

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


    def fetch_skin_table(self):
        loadout = self.fetch_loadout()['Guns']
        inventory = Loader.fetch_skin_data()
        loadout_patched = {}

        grid_order = [
            ["Classic", "Stinger", "Bulldog", "Marshal"],
            ["Shorty", "Spectre", "Guardian", "Operator"],
            ["Frenzy", "Bucky", "Phantom", "Ares"],
            ["Ghost", "Judge", "Vandal", "Odin"],
            ["Sheriff", None, None, "Melee"],
        ]
        grid_built = [[] for i in range(15)]

        longest = 0

        for weapon in loadout:
            weapon_data = inventory[weapon["ID"]]
            skin_data = weapon_data["skins"][weapon["SkinID"]]
            level_data = skin_data["levels"][weapon["SkinLevelID"]]
            chroma_data = skin_data["chromas"][weapon["ChromaID"]]

            loadout_patched[weapon_data["display_name"]] = {
                "ID": weapon["ID"],
                "skin_name": skin_data["display_name"],
                "level_name": level_data["display_name"],
                "chroma_name": chroma_data["display_name"],
                "color": skin_data["tier"]["color"]
            }
            if len(skin_data["display_name"]) > longest:
                longest = len(skin_data["display_name"])
            elif len(skin_data["display_name"]) > longest:
                longest = len(level_data["display_name"])
            elif len(skin_data["display_name"]) > longest:
                longest = len(chroma_data["display_name"])

        realrow = 0
        for row,guns in enumerate(grid_order):
            for col,weapon_name in enumerate(guns):
                if weapon_name is not None:
                    weapon_data = loadout_patched[weapon_name]
                    grid_built[realrow].append((f"{weapon_data['color']} bold",f"{weapon_data['skin_name']}\t".expandtabs(longest+4)))
                    grid_built[realrow+1].append((weapon_data["color"],f"{weapon_data['level_name']}\t".expandtabs(longest+4)))
                    grid_built[realrow+2].append((weapon_data["color"],f"{weapon_data['chroma_name']}\t".expandtabs(longest+4)))
                else:
                    grid_built[realrow].append(("White","\t".expandtabs(longest+4)))
                    grid_built[realrow+1].append(("White","\t".expandtabs(longest+4)))
                    grid_built[realrow+2].append(("White","\t".expandtabs(longest+4)))
                
            grid_built[realrow+2].append(("White","\n"))
            realrow += 3

        return grid_built

        # if only the api would return the guns in the right order :(


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
        