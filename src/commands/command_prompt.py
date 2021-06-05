
from termcolor import colored, cprint
from ..skin_manager.manager import Manager
from ..skin_manager.content import Content
from ..skin_manager.skin_loader import Loader
from ..game_listener.session import Session

#command imports 
from .set_skin import Set
from .help import Help

class Prompt:

    def __init__(self,auth_data=None,client=None):
        self.client = client
        self.manager = Manager(auth_data,client)
        self.content = Content()
        self.gun_pool = self.manager.fetch_gun_pool()

        #self.session = Session(client)

        # configuration stuffs
        self.auto_randomize = False

        self.help_data = {
            "set":{
                "desc":"set a gun's skin/level/chroma",
                "params":{
                    "[weapon_name]":"weapon's name (knife = melee)",
                    "[skin_name]":"skinline's name (reaver, prime)",
                    "(level_name)":"skin's upgrade level (defaults to 1)",
                    "(chroma_name)":"skin's chroma level (ex. 'blue', 'red'; defaults to Base)"
                },
                "bottom":"example: 'set vandal reaver 4 white'"
            },
            "help":{
                "desc":"overview of all commands",
                "commands":{
                    "help":"get this menu",
                    "set":"set a weapon's skin",
                    "randomize":"randomize each weapon's skin from the gun pool",
                    "loadout":"get the active skin loadout"
                },
                "bottom":"run 'setup' to set up your skin collection"
            },
            "loadout":{
                "desc":"get the active skin loadout",
            },
            "randomize":{
                "desc":"randomize your equipped skins",
            }
        }


    def main_loop(self):
        command = [""]
        cprint("VALORANT skin manager - type 'help' for help",attrs=["bold","underline"])
        while command[0] != "exit":
            command = input("> ").split()
            if command == []:
                command = [""]

            if command[0] == "help":
                Help(command,self.help_data)


            if command[0] == "loadout":
                table, longest = self.manager.fetch_skin_table()
                cprint(table.expandtabs(longest+3),"green")

            if command[0] == "setup":
                Loader.generate_skin_list()
                Loader.generate_skin_datas()

            if command[0] == "modify":
                Loader.generate_skin_datas()

            if command[0] == "set":
                Set(command,self.manager,self.content,self.gun_pool)
            
            if command[0] == "randomize":
                self.manager.randomize_skins() 
                cprint("randomized skins", "green", attrs=["bold"])
                table, longest = self.manager.fetch_skin_table()
                cprint(table.expandtabs(longest+4),"green")