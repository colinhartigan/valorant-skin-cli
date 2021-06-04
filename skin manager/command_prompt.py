
from termcolor import colored, cprint
from manager import Manager
from content import Content


class Prompt:

    def __init__(self):
        self.manager = Manager()
        self.content = Content()
        self.gun_pool = self.manager.fetch_gun_pool()


    def main_loop(self):
        command = [""]
        while command[0] != "exit":

            command = input("> ").split()

            if command[0] == "set":
                #format: set weanpon_name skin_name level chroma
                if len(command) != 5:
                    cprint("command missing params","red")
                    continue
                weapon_name = str(command[1])
                skin_name = str(command[2])

                try:
                    level_name = str(command[3])
                except:
                    cprint("no level provided, using default (lvl1)", "yellow")
                    level_name = "lvl1"
                try:
                    chroma_name = str(command[4])
                except:
                    cprint("no chroma provided, using default (Base)", "yellow")
                    chroma_name = "Base" #based

                #check input
                weapon = self.content.fetch_weapon_by_name(weapon_name)
                if weapon is not None:
                    weapon_skins = self.gun_pool[weapon['uuid']]

                    real_skin_name = ""
                    selected_skin = {}
                    selected_level = []
                    selected_chroma = []

                    for name,skin in weapon_skins.items():
                        if skin_name in name.lower():
                            selected_skin = skin
                            real_skin_name = name

                    if selected_skin != {}:
                        if len(selected_skin['levels']) > 1:
                            for level,uuid in selected_skin['levels'].items():
                                if level_name in level.lower():
                                    selected_level = [level,uuid] 
                        if len(selected_skin['levels']) == 1 or selected_level == []:
                            selected_level = ["lvl1",selected_skin['levels']['lvl1']]
                        
                        if len(selected_skin['chromas']) > 1:
                            for name,uuid in selected_skin['chromas'].items():
                                if chroma_name in name.lower():
                                    selected_chroma = [name,uuid]
                        if len(selected_skin['chromas']) == 1 or selected_chroma == []:
                            selected_level = ["Base",selected_skin['chromas']['Base']]

                        self.manager.modify_skin(weapon['uuid'],selected_skin['uuid'],selected_level[1],selected_chroma[1])
                       
                        cprint(f"{weapon['displayName']} -> {real_skin_name} ({selected_level[0]}/{selected_chroma[0]})","green",attrs=["bold"])
                    
                    else:
                        cprint("invalid skin; do you have it in the gun pool?", "red")
                
                else:
                    cprint("invalid weapon","red")


prompt = Prompt()
prompt.main_loop()