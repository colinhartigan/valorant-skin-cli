from valclient.client import Client
import threading
from termcolor import cprint
import sys

from src.cli.command_prompt import Prompt
from src.asynchronous.async_manager import Async_Manager

from src.flair_loader.skin_editor import Editor
from src.flair_loader.skin_loader import Loader

'''
TODO:
- skin pool change command should list a menu of guns then give options to set skins/chromas instead of going thru each gun
- spray randomizer extension for loadout randomizer
- gun pool skins should store all levels as a dict and say whether theyre enabled so its easier to modify what skins/levels/chromas are in the pool

- launch with valorant
- taskbar icon
'''

if __name__ == "__main__":
    client = Client()
    try:
        client.hook()
    except Exception as e:
        cprint(f"unable to launch: {e}", "red", "on_white", attrs=["bold"])
        sys.exit()

    Loader.generate_skin_data(client)
    Editor.select_weapon()

    '''
    loop = Async_Manager(client=client)
    async_thread = threading.Thread(target=loop.init_loop,daemon=True)
    async_thread.start()

    prompt = Prompt(client=client)
    cli_thread = threading.Thread(target=prompt.main_loop)
    cli_thread.start()
    '''
