import requests

class Skin_Content:

    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod
    def fetch_weapons_data():
        weapons_data = Skin_Content.fetch(f"/weapons")
        return weapons_data["data"]

    @staticmethod
    def fetch_skin_datas():
        skin_datas = Skin_Content.fetch(f"/weapons/skins")
        return skin_datas["data"]

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

    @staticmethod 
    def fetch_content_tiers():
        tiers = Skin_Content.fetch(endpoint=f"/contenttiers")
        return tiers["data"]

    @staticmethod 
    def fetch_gun_buddies():
        buddies = Skin_Content.fetch(endpoint=f"/buddies")
        return buddies["data"]