import requests

class Content:

    def __fetch(self,endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    def fetch_weapon_by_name(self,name):
        weapons = self.__fetch(endpoint="/weapons")["data"]

        for weapon in weapons:
            if name in weapon['displayName'].lower():
                return weapon
        return None