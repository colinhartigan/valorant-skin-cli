import json,os
from InquirerPy.utils import color_print

from ..entitlements.entitlement_manager import Entitlement_Manager
from ..content.skin_content import Skin_Content
from ..flair_management.gunbuddy_manager.buddy_manager import Buddies_Manager

from ..utility.logging import Logger
debug = Logger.debug

class Buddy_Loader:
    
    @staticmethod 
    def generate_buddy_data(client):
        buddy_entitlements = Entitlement_Manager.fetch_entitlements(client, "buddy")["Entitlements"]
        debug(f"buddy entitlements: {buddy_entitlements}")
        all_buddy_content = Skin_Content.fetch_gun_buddies()

        try:
            existing_buddy_data = Buddies_Manager.fetch_all_buddies()
        except:
            debug("buddy data integrity check failed!")
            color_print( [("Yellow bold", "[!] integrity check of buddy data file failed; generating fresh file")])
            existing_buddy_data = Buddies_Manager.generate_blank_buddies_file()

        sanitized_buddy_entitlements = {}
        for entitlement in buddy_entitlements:
            if not entitlement["ItemID"] in sanitized_buddy_entitlements.keys():
                sanitized_buddy_entitlements[entitlement["ItemID"]] = []
            sanitized_buddy_entitlements[entitlement["ItemID"]].append(entitlement["InstanceID"])

        new_buddy_data = {}

        for buddy in all_buddy_content:
            
            if buddy["levels"][0]["uuid"] in sanitized_buddy_entitlements.keys():
                buddy_already_exists = buddy["uuid"] in existing_buddy_data.keys()

                if not buddy_already_exists:
                    color_print([("Blue", f"new buddy found -> {buddy['displayName']}")])

                buddy_uuid = buddy["uuid"]
                buddy_data = {
                    "display_name": buddy["displayName"],
                    "enabled": True,
                    "instances": {
                        instance: {
                            "enabled": True,
                            "locked_weapon_uuid": ""
                        }
                        for instance in sanitized_buddy_entitlements[buddy["levels"][0]["uuid"]]
                    },
                    "level_uuid": buddy["levels"][0]["uuid"],
                }

                if buddy_already_exists:
                    buddy_data["enabled"] = existing_buddy_data[buddy["uuid"]]["enabled"]
                    buddy_data["instances"] = existing_buddy_data[buddy["uuid"]]["instances"]
                
                new_buddy_data[buddy_uuid] = buddy_data

        Buddies_Manager.modify_buddy_data(new_buddy_data)