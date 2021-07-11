from InquirerPy.utils import color_print
import sys,os

class Reload:

    def __init__(self):
        color_print([("LimeGreen","restarting...")])
        os.system('cls' if os.name == 'nt' else 'clear')
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 