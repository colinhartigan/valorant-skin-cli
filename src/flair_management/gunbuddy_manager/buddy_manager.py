# create dict of all gun buddies/uuids/names 

# can choose which buddies to include in randomizer pool
#   can lock gun's buddy, but this actually sets a value in the gunbuddy file, something like "locked_to" value

import os,json
import traceback
from InquirerPy.utils import color_print

from ...utility.logging import Logger
from ...utility.filepath import Filepath
debug = Logger.debug


class Buddies_Manager:

    @staticmethod
    def generate_blank_buddies_file():
        debug("generating blank gunbuddy file")
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'buddies.json')), 'w') as f:
            payload = []
            json.dump(payload, f)
            return payload

    @staticmethod
    def fetch_all_buddies():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'buddies.json')), 'r') as f:
                return json.load(f)
        except:
            color_print([("Yellow bold", "[!] integrity check of gun buddy data file failed; generating fresh file")])