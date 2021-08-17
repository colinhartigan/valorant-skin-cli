import os, sys, json
from InquirerPy.utils import color_print

class Program_Data:

    installs_path = os.path.expandvars("%PROGRAMDATA%\\valorant-tools\\installs.json")

    @staticmethod
    def update_file_location():
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        else:
            color_print([("Yellow","running in a non-frozen environment, cannot update installation path")])
            path = None

        if path is not None:
            installs = Program_Data.fetch_installs_file()
            installs["valorant-skin-cli"] = path
            Program_Data.modify_isntalls(installs)


    @staticmethod
    def fetch_installs_file():
        try:
            with open(Program_Data.installs_path) as f:
                installs = json.load(f)
                return installs
        except:
            return Program_Data.create_installs_file()

    @staticmethod
    def modify_isntalls(payload):
        with open(Program_Data.installs_path, "w") as f:
            json.dump(payload, f)

        return Program_Data.fetch_config()

    @staticmethod
    def create_installs_file():
        with open(Program_Data.installs_path, "w") as f:
            payload = {
                "valorant-skin-cli": ""
            }
            json.dump(payload, f)