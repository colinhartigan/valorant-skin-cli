from valclient.client import Client
from InquirerPy.utils import color_print

from src.startup import Startup
from src.utility.config_manager import default_config


# TODO:
# - launch with valorant
# - detect new releases on github
# - clarify some prompts

# TODO LATER:
# - loadouts


if __name__ == "__main__":

    color_print([("Tomato", f'''
 _   _____   __   ____  ___  ___   _  ________        __    _              ___    
| | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)   
| |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / /    
|___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/'''),("White",f"{default_config['version']}\n")])

    Startup.run()
 