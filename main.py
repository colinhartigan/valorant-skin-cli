from InquirerPy.utils import color_print
from InquirerPy import inquirer
import ctypes,os,traceback

from src.startup import Startup
from src.utility.config_manager import Config

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

if __name__ == "__main__":
    color_print([("Tomato", f""" _   _____   __   ____  ___  ___   _  ________        __    _              ___    
| | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)   
| |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / /    
|___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/"""),("White",f"{Config.default_config['version']}\n")])
    
    try:
        Startup.run()
    except:
        user32.ShowWindow(hWnd, 1)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        color_print([("Red bold","the program encountered an error; please create an issue with the traceback below if this problem persists")])
        traceback.print_exc()
        input("press enter to exit...")
        os._exit(1)