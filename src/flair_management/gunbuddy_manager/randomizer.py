from InquirerPy.utils import color_print
from .buddy_manager import Buddies_Manager
import random

class Buddy_Randomizer:

    @staticmethod
    def randomize(client):
        buddies = Buddies_Manager.fetch_all_buddies()
        loadout = client.fetch_player_loadout()
        #print(loadout)

        randomizer_pool = [
            {"buddy_uuid": buddy, "level_uuid": data["level_uuid"], "instances": [uuid for uuid,instance in data["instances"].items() if instance["enabled"] and instance["locked_weapon_uuid"] == ""]} for buddy,data in buddies.items() if data["enabled"] and len([instance for _,instance in data["instances"].items() if instance["enabled"] and instance["locked_weapon_uuid"] == ""]) > 0
        ]
        #print(randomizer_pool)
        locked_weapons = {}

        for uuid,buddy in buddies.items():
            for i_uuid,instance in buddy["instances"].items():
                if instance["locked_weapon_uuid"] != "":
                    locked_weapons[instance["locked_weapon_uuid"]] = {
                        "buddy_uuid": uuid,
                        "level_uuid": buddy["level_uuid"],
                        "instance_uuid": i_uuid
                    }

        
        for weapon in loadout["Guns"]:
            if weapon["ID"] != "2f59173c-4bed-b6c3-2191-dea9b58be9c7":
                if weapon["ID"] in locked_weapons:
                    weapon["CharmID"] = locked_weapons[weapon["ID"]]["buddy_uuid"]
                    weapon["CharmLevelID"] = locked_weapons[weapon["ID"]]["level_uuid"]
                    weapon["CharmInstanceID"] = locked_weapons[weapon["ID"]]["instance_uuid"]

                else:
                    try:
                        buddy_index = random.randrange(0,len(randomizer_pool))
                        buddy_data = randomizer_pool[buddy_index]
                        
                        weapon["CharmID"] = buddy_data["buddy_uuid"]
                        weapon["CharmLevelID"] = buddy_data["level_uuid"]
                        weapon["CharmInstanceID"] = buddy_data["instances"][0]
                        
                        buddy_data["instances"].pop(0)

                        if len(buddy_data["instances"]) == 0:
                            randomizer_pool.pop(buddy_index)
                    except:
                        break

        client.put_player_loadout(loadout=loadout)
        color_print([("Lime", "randomized buddies")])