import requests 
from InquirerPy.utils import color_print

class Checker:
    @staticmethod 
    def check_version(config):
        if not config["meta"]["surpress_update_notifications"]:
            current_version = config["version"]
            data = requests.get("https://api.github.com/repos/colinhartigan/valorant-skin-cli/releases/latest")
            latest = data.json()["tag_name"]
            if latest != current_version:
                color_print([("Yellow bold",f"an update is available ({current_version} -> {latest})! download it at "),("Cyan underline",f"https://github.com/colinhartigan/valorant-skin-cli/releases/tag/{latest}")])