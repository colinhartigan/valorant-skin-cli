from valclient.client import Client
import threading
from InquirerPy.utils import color_print
import sys

from src.startup import Startup


# TODO:
# - launch with valorant
# - taskbar icon


if __name__ == "__main__":

    color_print([("Tomato", '''
      _   _____   __   ____  ___  ___   _  ________        __    _              ___    
     | | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)   
     | |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / /    
     |___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/     
    ''')])

    Startup.run()
