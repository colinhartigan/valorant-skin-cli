from termcolor import cprint

class Set:
    def __init__(self,command,manager,content,gun_pool):

        # format: set weanpon_name skin_name level chroma
        if len(command) < 3:
            cprint("command missing required params", "red")
            return
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
            chroma_name = "Base"  # based

        # check input
        weapon = content.fetch_weapon_by_name(weapon_name)
        if weapon is not None:
            weapon_skins = gun_pool[weapon['uuid']]

            real_skin_name = ""
            selected_skin = {}
            selected_level = []
            selected_chroma = []

            for name, skin in weapon_skins.items():
                if skin_name in name.lower():
                    selected_skin = skin
                    real_skin_name = name

            if selected_skin != {}:
                if len(selected_skin['levels']) > 1:
                    for level, uuid in selected_skin['levels'].items():
                        if level_name in level.lower():
                            selected_level = [level, uuid]
                if selected_level == []:
                    selected_level = ["lvl1", selected_skin['levels']['lvl1']]

                if len(selected_skin['chromas']) > 1:
                    for name, uuid in selected_skin['chromas'].items():
                        if chroma_name in name.lower():
                            selected_chroma = [name, uuid]
                if selected_chroma == []:
                    selected_chroma = ["Base", selected_skin['chromas']['Base']]

                manager.modify_skin(
                    weapon['uuid'], selected_skin['uuid'], selected_level[1], selected_chroma[1])

                cprint(
                    f"{weapon['displayName']} -> {real_skin_name} ({selected_level[0]}/{selected_chroma[0]})", "green", attrs=["bold"])

            else:
                cprint("invalid skin; do you have it in the gun pool?", "red")

        else:
            cprint("invalid weapon", "red")
