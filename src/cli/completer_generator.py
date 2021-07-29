from ..flair_loader.skin_loader_withcheck import Skin_Loader
from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..flair_management.loadout_manager.loadouts_manager import Loadouts_Manager

class Completer:

    cli = None

    @staticmethod
    def generate_completer_dict():
        '''Generate command autocomplete data'''
        data = {
            "randomize": None,
            "modify": None,
            "reset": None,
            "loadout": {},
            "config": None,
            "set": {},
            "reload": None,
            "exit": None,
        }

        # generate autocomplete for "set" command        
        # im actually so happy this worked; made validation for setting skins SO easy to implement
        def build_set_autocomplete():
            skin_data = Skin_Manager.fetch_skin_data()
            weapons = {}
            for uuid,weapon in skin_data.items():
                weapons[weapon['display_name']] = {
                    skin['display_name'].replace(" ","-"): {
                        level['display_name'].replace(" ","-"): {
                            chroma['display_name'].replace(" ","-"): {} for _,chroma in skin['chromas'].items()
                        } for _,level in skin['levels'].items()
                    } for _,skin in weapon['skins'].items()
                }
            data['set'] = weapons

        def build_loadout_autocomplete():
            data["loadout"] = {
                "create": None,
                "equip": {},
                "preview": {},
                "delete": {},
            }

            loadouts = Loadouts_Manager.fetch_all_loadouts()
            if loadouts is not None:
                for loadout in loadouts:
                    data["loadout"]["equip"][loadout["name"].replace(" ", "-")] = None  
                    data["loadout"]["preview"][loadout["name"].replace(" ", "-")] = None  
                    data["loadout"]["delete"][loadout["name"].replace(" ", "-")] = None  

        build_set_autocomplete()
        build_loadout_autocomplete()

        Completer.cli.commands = data
        return data