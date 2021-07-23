import requests

class Identity_Content:

    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod
    def fetch_spray_data():
        sprays_data = Identity_Content.fetch(f"/sprays")
        return sprays_data["data"]

    def fetch_card_by_id(uuid):
        card_data = Identity_Content.fetch(f"/playercards/{uuid}")
        return card_data["data"]

    def fetch_title_by_id(uuid):
        title_data = Identity_Content.fetch(f"/playertitles/{uuid}")
        return title_data["data"]