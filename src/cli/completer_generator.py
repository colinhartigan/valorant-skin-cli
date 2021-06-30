from ..flair_loader.skin_loader import Loader


class Completer:

    @staticmethod
    def generate_completer_dict():
        '''Generate command autocomplete data'''
        data = {
            "randomize": None,
            "modify": None,
            "loadout": None,
            "exit": None,
            "set": {}
        }

        skin_data = Loader.fetch_skin_data()
        
        weapons = {

        }
        for uuid,weapon in skin_data.items():
            weapons[weapon['display_name']] = {
               skin['display_name'].replace(" ","-"): {
                   level['display_name'].replace(" ","-"): {
                       chroma['display_name'].replace(" ","-"): {} for _,chroma in skin['chromas'].items()
                   } for _,level in skin['levels'].items()
               } for _,skin in weapon['skins'].items()
            }

        data['set'] = weapons

        return data