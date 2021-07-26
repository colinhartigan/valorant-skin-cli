from InquirerPy.utils import color_print
from ...flair_management.skin_manager.skin_manager import Skin_Manager

class Set_Skin:
    def __init__(self, client, command):
        
        inventory_data = Skin_Manager.fetch_skin_data()
        # format: set weanpon_name skin_name level chroma
        if len(command) < 3:
            color_print([("#f44336","command missing required params")])
            return
        weapon_name = str(command[1])
        skin_name = str(command[2]).replace("-"," ")

        weapon_data = ()
        skin_data = ()
        level_data = ()
        chroma_data = ()
        for uuid,weapon in inventory_data.items():
            if weapon["display_name"] == weapon_name:
                weapon_data = (uuid,weapon) 

        for uuid,skin in weapon_data[1]["skins"].items():
            if skin["display_name"] == skin_name:
                skin_data = (uuid,skin)

        if len(command) < 4:
            # missing level
            level_data = (list(skin_data[1]["levels"].keys())[-1],skin_data[1]["levels"][list(skin_data[1]["levels"].keys())[-1]])
            if len(skin_data[1]["levels"]) > 1:
                color_print([("Yellow italic",f"no level provided, using default ({level_data[1]['display_name']})")])
        else:
            level_name = command[3].replace("-"," ")
            for uuid,level in skin_data[1]["levels"].items():
                if level['display_name'] == level_name:
                    level_data = (uuid,level)

        if len(command) < 5:
            # missing chroma
            chroma_data = (list(skin_data[1]["chromas"].keys())[-1],skin_data[1]["chromas"][list(skin_data[1]["chromas"].keys())[-1]])
            if len(skin_data[1]["chromas"]) > 1:
                color_print([("Yellow italic",f"no chroma provided, using default ({chroma_data[1]['display_name']})")])
        else:
            chroma_name = command[4].replace("-"," ") 
            for uuid,chroma in skin_data[1]["chromas"].items():
                if chroma['display_name'] == chroma_name:
                    chroma_data = (uuid,chroma)


        Skin_Manager.modify_skin(client,weapon_data[0], skin_data[0], level_data[0], chroma_data[0])
        color_print([("Lime bold",f"{weapon_data[1]['display_name']} -> {skin_data[1]['display_name']} ({level_data[1]['display_name']}/{chroma_data[1]['display_name']})")])
        