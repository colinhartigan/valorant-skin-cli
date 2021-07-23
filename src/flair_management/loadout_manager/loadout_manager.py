import os,json

from ...utility.logging import Logger
from ...utility.filepath import Filepath
debug = Logger.debug


class Loadout_Manager:

    @staticmethod
    def generate_blank_loadouts_file():
        debug("generating blank loadouts file")
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'loadouts.json')), 'w') as f:
            pass