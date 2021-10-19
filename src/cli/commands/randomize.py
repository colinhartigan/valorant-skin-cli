from InquirerPy.utils import color_print
import sys,os

from ...flair_management.skin_manager.randomizer import Skin_Randomizer 
from ...flair_management.gunbuddy_manager.randomizer import Buddy_Randomizer

class Randomize:

    def __init__(self,command,client,config):
        
        if len(command) != 2:
            if config["skin_randomizer"]["enabled"]:
                Skin_Randomizer.randomize(client)
            if config["buddy_randomizer"]["enabled"]:
                Buddy_Randomizer.randomize(client)
        else:
            if command[1] == "skins": 
                Skin_Randomizer.randomize(client)
            elif command[1] == "buddies":
                Buddy_Randomizer.randomize(client)