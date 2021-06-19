
class Entitlement_Manager:

    @staticmethod 
    def fetch_entitlements(client,entitlement_type):
        conversions = {
            "e7c63390-eda7-46e0-bb7a-a6abdacd2433": "skin_level",
            "3ad1b2b2-acdb-4524-852f-954a76ddae0a": "skin_chroma",
            "01bb38e1-da47-4e6a-9b3d-945fe4655707": "agent",
            "f85cb6f7-33e5-4dc8-b609-ec7212301948": "contract_definition",
            "dd3bf334-87f3-40bd-b043-682a57a8dc3a": "buddy",
            "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": "spray",
            "3f296c07-64c3-494c-923b-fe692a4fa1bd": "player_card",
            "de7caa6b-adf7-4588-bbd1-143831e786c6": "player_title",
        }
        for i,v in conversions.items():
            if entitlement_type.lower() in v:
                item_type = i 
                return client.fetch_store_entitlements(item_type=item_type)
        return None