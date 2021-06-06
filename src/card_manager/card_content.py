import requests

class Card_Content:

    @staticmethod
    def fetch(endpoint="/"):
        data = requests.get(f"https://valorant-api.com/v1{endpoint}")
        return data.json()

    @staticmethod 
    def fetch_card_by_name(name):
        cards = Card_Content.fetch(endpoint="/playercards")["data"]

        for card in cards:
            if name in card['displayName'].lower():
                return card
        return None

    @staticmethod 
    def fetch_all_cards():
        cards = Card_Content.fetch(endpoint="/playercards")["data"]
        return cards 