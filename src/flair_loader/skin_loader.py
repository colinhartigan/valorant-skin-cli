import json
import os
from termcolor import cprint

from ..content.skin_content import Skin_Content
from ..entitlements.entitlement_manager import Entitlement_Manager


class Loader:

    @staticmethod
    def sanitize_chroma_name(skin, chroma, weapon_name):
        try:
            new = chroma
            new = new.rstrip("\\r\\n")
            new = new.strip(weapon_name)
            new = new[new.find("(") + 1:new.find(")")]
            if new in skin['displayName']:
                new = "Base"
            return new
        except:
            return "Base"

    @staticmethod
    def fetch_content_tier(tiers, uuid):

        # define skin tier indices for sorting skins

        tier_indices = {
            "Standard": 0,
            "Battlepass": 1,
            "Select": 2,
            "Deluxe": 3,
            "Premium": 4,
            "Exclusive": 5,
            "Ultra": 6,
        }

        if uuid not in ('standard', 'bp'):
            for tier in tiers:
                if tier["uuid"] == uuid:
                    tier["index"] = tier_indices[tier["devName"]]
                    return tier
        elif uuid == "standard":
            return {
                "devName": "Standard",
                "highlightColor": "474747",
                "index": tier_indices["Standard"]
            }
        elif uuid == "bp":
            return {
                "devName": "Battlepass",
                "highlightColor": "66C3A9",
                "index": tier_indices["Battlepass"]
            }

    @staticmethod
    def generate_skin_data(client):
        skin_level_entitlements = Entitlement_Manager.fetch_entitlements(client, "skin_level")
        skin_chroma_entitlements = Entitlement_Manager.fetch_entitlements(client, "skin_chroma")
        content_tiers = Skin_Content.fetch_content_tiers()
        all_weapon_content = Skin_Content.fetch_weapon_datas()

        existing_skin_data = {}
        # check integrity of existing skin data and/or if it exists, if not, start new data
        try:
            existing_skin_data = Loader.fetch_skin_data()
        except:
            cprint("[!] integrity check of skin data file failed; generating fresh data", "yellow", attrs=["bold"])
            existing_skin_data = Loader.generate_blank_skin_file()

        new_skin_data = {}

        for weapon in all_weapon_content:
            # cprint(f"[{weapon['displayName']}] generating skin data","green",attrs=["bold"])

            weapon_uuid = weapon["uuid"]
            weapon_data = {
                "display_name": weapon["displayName"],
                "weapon_type": weapon["category"].replace('EEquippableCategory::', ''),
                "skins": {}
            }

            for skin in weapon["skins"]:
                if skin["displayName"] == "Melee":
                    # why is rito so inconsistent
                    skin["displayName"] = "Standard Melee"
                    skin["chromas"][0]["displayName"] = "Melee"
                    skin["levels"][0]["displayName"] = "Melee"

                skin_owned = False
                skin_previously_owned = False
                skin_uuid = skin["uuid"]
                skin_tier_data = Loader.fetch_content_tier(content_tiers, skin["contentTierUuid"] if skin[
                                                                                                         "contentTierUuid"] is not None else "standard" if "Standard" in
                                                                                                                                                           skin[
                                                                                                                                                               "displayName"] else "bp")

                for level in skin["levels"]:
                    for entitlement in skin_level_entitlements["Entitlements"]:
                        if level is not None and entitlement["ItemID"] == level["uuid"]:
                            skin_owned = True
                            break

                if "Standard" in skin["displayName"]:
                    # enable if base skin
                    skin_owned = True

                if skin["uuid"] in existing_skin_data[weapon_uuid]["skins"]:
                    # check if there was already skin data in old backup file
                    skin_previously_owned = True

                if skin_owned:

                    if not skin_previously_owned:
                        cprint(f"[{weapon['displayName']}] new skin found -> {skin['displayName']}", "blue")

                    weapon_data["skins"][skin_uuid] = {
                        "display_name": skin["displayName"],
                        "enabled": False if not skin_previously_owned else
                        existing_skin_data[weapon_uuid]["skins"][skin_uuid]['enabled'],
                        "tier": {
                            "display_name": skin_tier_data["devName"],
                            "color": skin_tier_data["highlightColor"],
                            "tier_index": skin_tier_data["index"],
                        },
                        "levels": {},
                        "chromas": {},
                    }

                    for level in skin["levels"]:
                        level_already_exists = skin_previously_owned and level["uuid"] in \
                                               existing_skin_data[weapon_uuid]["skins"][skin_uuid]["levels"]

                        def process_skin_level():
                            if level_already_exists:
                                weapon_data["skins"][skin_uuid]["levels"][level["uuid"]] = \
                                    existing_skin_data[weapon_uuid]["skins"][skin_uuid]["levels"][level["uuid"]]

                            else:
                                weapon_data["skins"][skin_uuid]["levels"][level["uuid"]] = {
                                    "display_name": f"{level['displayName']}" + (
                                        f" ({level['levelItem'].replace('EEquippableSkinLevelItem::', '')})" if level[
                                                                                                                    'levelItem'] is not None else "" if
                                        level["displayName"] == skin["displayName"].replace("Standard ",
                                                                                            "") else " (VFX)" if level[
                                                                                                                     'displayName'] !=
                                                                                                                 skin[
                                                                                                                     'displayName'] else ""),
                                    "enabled": False
                                }
                                cprint(f"[{skin['displayName']}] found new level data ({level['displayName']})", "cyan")

                        if level is not None and level["displayName"] == skin["displayName"].replace("Standard ", ""):
                            # if skin is standard
                            process_skin_level()
                        else:
                            for entitlement in skin_level_entitlements["Entitlements"]:
                                if level is not None and entitlement["ItemID"] == level["uuid"]:
                                    process_skin_level()

                    for chroma in skin["chromas"]:
                        chroma_already_exists = skin_previously_owned and chroma["uuid"] in \
                                                existing_skin_data[weapon_uuid]["skins"][skin_uuid]["chromas"]

                        def process_chroma():
                            if chroma_already_exists:
                                weapon_data["skins"][skin_uuid]["chromas"][chroma["uuid"]] = \
                                    existing_skin_data[weapon_uuid]["skins"][skin_uuid]["chromas"][chroma["uuid"]]
                            else:
                                weapon_data["skins"][skin_uuid]["chromas"][chroma["uuid"]] = {
                                    "display_name": Loader.sanitize_chroma_name(skin, chroma["displayName"],
                                                                                weapon["displayName"]),
                                    "enabled": False
                                }
                                cprint(
                                    f"[{skin['displayName']}] found new chroma data ({Loader.sanitize_chroma_name(skin, chroma['displayName'], weapon['displayName'])})",
                                    "cyan")

                        if chroma["displayName"] == skin["displayName"].replace("Standard ", ""):
                            process_chroma()
                        elif chroma["displayName"] == skin["displayName"] or chroma["displayName"] is None:
                            process_chroma()
                        else:
                            for entitlement in skin_chroma_entitlements["Entitlements"]:
                                if chroma is not None and entitlement["ItemID"] == chroma["uuid"]:
                                    process_chroma()

                    # enable base level/chroma
                    # print(weapon_data["skins"][skin_uuid])
                    weapon_data["skins"][skin_uuid]["levels"][
                        list(weapon_data["skins"][skin_uuid]["levels"].keys())[-1]]['enabled'] = True
                    weapon_data["skins"][skin_uuid]["chromas"][
                        list(weapon_data["skins"][skin_uuid]["chromas"].keys())[-1]]['enabled'] = True

                    # sort skins by tier index
            weapon_data["skins"] = dict(
                sorted(weapon_data["skins"].items(), key=lambda skin: skin[1]['tier']['tier_index'], reverse=True))
            new_skin_data[weapon_uuid] = weapon_data

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'skin_data.json')), 'w') as f:
            json.dump(new_skin_data, f)
            cprint("skins loaded!", "green", attrs=["bold"])

    @staticmethod
    def generate_blank_skin_file():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'skin_data.json')), 'w') as f:
            new_data = {}

            all_weapon_content = Skin_Content.fetch_weapon_datas()
            for weapon in all_weapon_content:
                weapon_uuid = weapon["uuid"]
                weapon_data = {
                    "display_name": weapon["displayName"],
                    "skins": {}
                }

                new_data[weapon_uuid] = weapon_data

            json.dump(new_data, f)

        return Loader.fetch_skin_data()

    @staticmethod
    def modify_skin_data(new_data):
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'skin_data.json')), 'w') as f:
            json.dump(new_data, f)

    @staticmethod
    def fetch_skin_data():
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data', 'skin_data.json'))) as f:
            return json.load(f)
