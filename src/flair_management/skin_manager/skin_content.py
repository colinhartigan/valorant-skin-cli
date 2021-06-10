import requests

class Skin_Content:


    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod
    def fetch_weapon_datas():
        weapon_datas = Skin_Content.fetch(f"/weapons")
        return weapon_datas["data"]

    @staticmethod
    def fetch_skin_datas():
        skin_datas = Skin_Content.fetch(f"/weapons/skins")
        return skin_datas["data"]

    @staticmethod
    def fetch_weapon_by_name(name):
        weapons = Skin_Content.fetch(endpoint="/weapons")["data"]

        for weapon in weapons:
            if name in weapon['displayName'].lower():
                return weapon
        return None

    @staticmethod 
    def fetch_weapon_by_id(uuid):
        weapon = Skin_Content.fetch(endpoint=f"/weapons/{uuid}")
        return weapon['data']

    @staticmethod
    def fetch_skin_by_id(uuid):
        skin = Skin_Content.fetch(endpoint=f"/weapons/skins/{uuid}")
        return skin['data']

    @staticmethod 
    def fetch_chroma_by_id(uuid):
        skin = Skin_Content.fetch(endpoint=f"/weapons/skinchromas/{uuid}")
        return skin['data']

    @staticmethod 
    def fetch_level_by_id(uuid):
        skin = Skin_Content.fetch(endpoint=f"/weapons/skinlevels/{uuid}")
        return skin['data']