from src.cli.command_prompt import Prompt 
from src.asynchronous.async_manager import Async_Manager

from valclient.client import Client
import threading

'''
TODO:
- skin pool change command should list a menu of guns then give options to set skins/chromas instead of going thru each gun
- spray randomizer extension for loadout randomizer

- launch with valorant
- taskbar icon
- (implement RPC?) probably make this a diff module as an extension
'''

if __name__ == "__main__":
    client = Client()
    client.hook()

    loop = Async_Manager(client=client)
    async_thread = threading.Thread(target=loop.init_loop,daemon=True)
    async_thread.start()

    prompt = Prompt(client=client)
    cli_thread = threading.Thread(target=prompt.main_loop)
    cli_thread.start()