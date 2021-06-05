import requests
from termcolor import colored, cprint
import json
import os
from .content import Content

here = os.path.dirname(os.path.abspath(__file__))

class Loader:
        
    @staticmethod
    def generate_skin_list():
        cprint("SKIN COLLECTION SETUP","yellow",attrs=["bold"])
        weapon_datas = Content.fetch_weapon_datas()
        payload = {}

        for weapon in weapon_datas:
            weapon_uuid = weapon['uuid']
            cprint(f"[{weapon['displayName']}] which skins do you want to include in the pool for this gun? (separate skins with comma ex. 'reaver,prime')","green")
            themes = input("> ").split(",")

            payload[weapon_uuid] = themes  

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'included_skins.json')), 'w') as f:
            json.dump(payload, f)
            cprint("done","blue",attrs=["bold"])

    @staticmethod
    def sanitize_chroma_name(skin,chroma,weapon_name):
        try:
            new = chroma 
            new = new.rstrip("\\r\\n")
            new = new.strip(weapon_name)
            new = new[new.find("(")+1:new.find(")")]
            if new in skin['displayName']:
                new = "Base"
            return new
        except:
            return "Base"

    @staticmethod
    def generate_skin_datas():
        cprint("SKIN DATA SETUP","yellow",attrs=["bold"])
        weapon_datas = Content.fetch_weapon_datas()
        payload = {}
        skin_pool = {}

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'included_skins.json'))) as f:
            skin_pool = json.load(f)

        level_type = ""
        while (level_type == "") and (level_type != "y" or level_type != "n"):
            cprint("[Leveling] 1/2: include (1) all levels or (2) only max level? (for upgradable skins)","yellow")
            level_type = str(input("> "))

        for weapon in weapon_datas:
            #print(weapon)
            payload[weapon['uuid']] = {}
            cprint(f"[{weapon['displayName']}] loading requested skins","green",attrs=["bold"])

            skins = weapon['skins']

            themes = skin_pool[weapon['uuid']]
            for theme in themes:
                if theme == "":
                    continue
                for skin in skins:
                    if theme in skin['displayName'].lower():
                        
                        cprint(f"[{weapon['displayName']}] generating data for {skin['displayName']}","cyan")

                        chromas = {}

                        if len(skin['chromas']) > 1:
                            cprint(f"[{skin['displayName']}] which chromas do you want to include? (press enter for all or type the number(s) separated by commas)","yellow")
                            print("\n".join(f"{i} - {Loader.sanitize_chroma_name(skin,v['displayName'],weapon['displayName'])}" for i,v in enumerate(skin['chromas'])))
                            
                            choices = input("> ")
                            if choices == "" or choices == " ":
                                chromas = {Loader.sanitize_chroma_name(skin,i['displayName'],weapon['displayName']) : i['uuid'] for i in skin['chromas']}
                            else:
                                choices = [int(i) for i in choices.strip().split(",")]
                                for i,v in enumerate(skin['chromas']):
                                    if i in choices:
                                        chromas[Loader.sanitize_chroma_name(skin,v['displayName'],weapon['displayName'])] = v['uuid']
                        else:
                            chromas = {Loader.sanitize_chroma_name(skin,i['displayName'],weapon['displayName']) : i['uuid'] for i in skin['chromas']}

                        levels = {}
                        if level_type == "1":
                            levels = {f"lvl{i+1}": v['uuid'] for i,v in enumerate(skin['levels'])}
                        else:
                            levels = {f"lvl{len(skin['levels'])}" : skin['levels'][-1]['uuid']}
                                                    

                        payload[weapon['uuid']][skin['displayName']] = {
                            "uuid": skin['uuid'],
                            "levels": levels,
                            "chromas": chromas
                        }
                        
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'gun_pool.json')), 'w') as f:
            json.dump(payload, f)
        cprint("done!","blue",attrs=['bold'])
        
