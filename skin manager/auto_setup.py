import requests
from termcolor import colored, cprint
import json
import os

here = os.path.dirname(os.path.abspath(__file__))

class skin_loader:
    @staticmethod
    def get_weapon_datas():
        weapon_datas = requests.get(f"https://valorant-api.com/v1/weapons")
        weapon_datas = weapon_datas.json()['data']
        return weapon_datas
        
    @staticmethod
    def generate_skin_lists():
        weapon_datas = skin_loader.get_weapon_datas()
        payload = {}

        for weapon in weapon_datas:
            weapon_uuid = weapon['uuid']
            print(f"[{weapon['displayName']}] which skins do you want to include in the pool for this gun?")
            themes = input("skins: ").split(",")

            payload[weapon_uuid] = themes  

        with open(os.path.join(here, 'skins.json'), 'w') as f:
            json.dump(payload, f)
            print("done")

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
        weapon_datas = skin_loader.get_weapon_datas()
        payload = {}
        skin_pool = {}

        with open(os.path.join(here, 'skins.json')) as f:
            skin_pool = json.load(f)

        for weapon in weapon_datas:
            #print(weapon)
            payload[weapon['uuid']] = {}
            cprint(f"[{weapon['displayName']}] loading requested skins","green","on_grey",attrs=["bold"])

            skins = weapon['skins']

            themes = skin_pool[weapon['uuid']]
            for theme in themes:
                for skin in skins:
                    if theme in skin['displayName'].lower():
                        
                        cprint(f"[{weapon['displayName']}] generating data for {skin['displayName']}","cyan")

                        chromas = {}

                        if len(skin['chromas']) > 1:
                            cprint(f"[{skin['displayName']}] which chromas do you want to include? (press enter for all or type the number(s) separated by commas)","yellow")
                            print("\n".join(f"{i} - {skin_loader.sanitize_chroma_name(skin,v['displayName'],weapon['displayName'])}" for i,v in enumerate(skin['chromas'])))
                            
                            choices = input()
                            if choices == "" or choices == " ":
                                chromas = {skin_loader.sanitize_chroma_name(skin,i['displayName'],weapon['displayName']) : i['uuid'] for i in skin['chromas']}
                            else:
                                choices = [int(i) for i in choices.strip().split(",")]
                                for i,v in enumerate(skin['chromas']):
                                    if i in choices:
                                        chromas[skin_loader.sanitize_chroma_name(skin,v['displayName'],weapon['displayName'])] = v['uuid']
                        else:
                            chromas = {skin_loader.sanitize_chroma_name(skin,i['displayName'],weapon['displayName']) : i['uuid'] for i in skin['chromas']}


                        payload[weapon['uuid']][skin['displayName']] = {
                            "uuid": skin['uuid'],
                            "levels": {f"lvl{i+1}": v['uuid'] for i,v in enumerate(skin['levels'])},
                            "chromas": chromas
                        }
                        

        cprint("done!","blue",attrs=['bold'])
        print(json.dumps(payload, indent=4))

skin_loader.generate_skin_datas()
