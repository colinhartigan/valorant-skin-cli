import os
import json
from InquirerPy.utils import color_print

from ...utility.logging import Logger
from ...utility.filepath import Filepath
debug = Logger.debug


class Loadouts_Manager:

    @staticmethod
    def generate_blank_loadouts_file():
        debug("generating blank loadouts file")
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'loadouts.json')), 'w') as f:
            payload = []
            json.dump(payload, f)
            return payload

    @staticmethod
    def fetch_all_loadouts():
        try:
            with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'loadouts.json')), 'r') as f:
                return json.load(f)
        except:
            color_print([("Yellow bold", "[!] integrity check of loadout data file failed; generating fresh file")])
            Loadouts_Manager.generate_blank_loadouts_file()

    @staticmethod
    def fetch_loadout_by_name(loadout_name):
        loadouts = Loadouts_Manager.fetch_all_loadouts()
        for loadout in loadouts:
            if loadout["name"] == loadout_name:
                return loadout

    @staticmethod
    def add_loadout(loadout_data):
        loadouts = Loadouts_Manager.fetch_all_loadouts()
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'loadouts.json')), 'w') as f:
            loadouts.append(loadout_data)
            json.dump(loadouts, f)

    def remove_loadout(loadout_name):
        loadouts = Loadouts_Manager.fetch_all_loadouts()
        for loadout in loadouts:
            if loadout["name"] == loadout_name:
                target = loadout
        loadouts.remove(target)
        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'loadouts.json')), 'w') as f:
            json.dump(loadouts, f)
            return loadouts