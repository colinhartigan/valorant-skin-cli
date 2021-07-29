from InquirerPy.utils import color_print
from .buddy_manager import Buddies_Manager
import random

class Buddy_Randomizer:

    @staticmethod
    def randomize(client):
        buddies = Buddies_Manager.fetch_all_buddies()
        loadout = client.fetch_player_loadout()

        randomizer_pool = {
            buddy: {"level_uuid": data["level_uuid"], "instances": [uuid for uuid,instance in data["instances"].items() if instance["enabled"] and instance["locked_weapon_uuid"] == ""]} for buddy,data in buddies.items() if data["enabled"] and len([instance for uuid,instance in data["instances"].items() if instance["enabled"] and instance["locked_weapon_uuid"] == ""]) > 0
        }
        locked_instances = {
            # write this
        }
        