from ..flair_loader.skin_loader import Loader

class Completer:

    @staticmethod
    def generate_completer_dict():
        '''Generate command autocomplete data'''
        data = {
            "randomize": None,
            "modify": None,
            "help": None,
            "exit": None,
            "set": {}
        }

        skin_data = Loader.fetch_skin_data()
        #print(skin_data)
        return data