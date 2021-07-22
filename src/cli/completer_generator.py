from ..flair_loader.skin_loader_withcheck import Loader


class Completer:

    @staticmethod
    def generate_completer_dict():
        '''Generate command autocomplete data'''
        data = {
            "randomize": None,
            "modify": None,
            "loadout": None,
            "config": None,
            "set": {},
            "reload": None,
            "exit": None,
        }

        # generate autocomplete for "set" command
        skin_data = Loader.fetch_skin_data()
        weapons = {}
        
        # im actually so happy this worked; made validation for setting skins SO easy to implement
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