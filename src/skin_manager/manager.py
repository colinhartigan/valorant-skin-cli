from valclient.client import Client
import os 
import json
import random
import requests
from termcolor import colored, cprint
from .content import Content
from .skin_loader import Loader

here = os.path.dirname(os.path.abspath(__file__))

class Manager:

    def __init__(self,auth_data=None,client=None):
        self.client = client

    def fetch_loadout(self):
        # make a better version that prints in gun -> skin format
        return self.client.fetch_player_loadout()

    def put_loadout(self,loadout):
        return self.client.put_player_loadout(loadout=loadout)

    def fetch_gun_pool(self):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'gun_pool.json'))) as f:
            gun_pool = json.load(f)
            return gun_pool

    def fetch_weapon_data(self,weapon_uuid,weapon_datas):
        for i in weapon_datas:
            if i['uuid'] == weapon_uuid:
                return i

    def fetch_skin_data(self,skin_uuid,skin_datas):
        for i in skin_datas:
            if i['uuid'] == skin_uuid:
                return i


    def fetch_skin_table(self):
        loadout = self.fetch_loadout()['Guns']
        skins = {}
        grid = {}

        longest = 0

        weapons_datas = Content.fetch_weapon_datas()
        skins_datas = Content.fetch_skin_datas()

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
        loadout = self.fetch_loadout()

        weapon_datas = requests.get(f"https://valorant-api.com/v1/weapons")
        weapon_datas = weapon_datas.json()['data']

        gun_pool = self.fetch_gun_pool()
        for i in loadout['Guns']:
            weapon_uuid = i['ID']

            weapon_data = self.fetch_weapon_data(weapon_uuid,weapon_datas)
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

        new = self.put_loadout(loadout=loadout)