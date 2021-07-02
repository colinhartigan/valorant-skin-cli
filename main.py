from valclient.client import Client
import threading
from termcolor import cprint
import sys

from src.cli.command_prompt import Prompt
from src.asynchronous.async_manager import Async_Manager

from src.flair_loader.skin_editor import Editor
from src.flair_loader.skin_loader import Loader

from src.utility.config_manager import Config
from src.utility.onboarding import Onboarder

'''
TODO:

- launch with valorant
- taskbar icon
'''

if __name__ == "__main__":

    cprint(
'''     _   _____   __   ____  ___  ___   _  ________        __    _              ___ 
    | | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)
    | |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / / 
    |___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/  
''',"red",
    )

    config = Config.fetch_config()

    region = config["region"].lower()
    client = Client(region=region)
    try:
        client.hook()
    except Exception as e:
        cprint(f"unable to launch: {e}", "red", "on_white", attrs=["bold"])
        sys.exit()

    if not config["meta"]["onboarding_completed"]:
        Onboarder(client)
        # reset the client if region changed during onboarding
        config = Config.fetch_config()
        client = Client(region=region)
        client.hook()

    # load skin data
    Loader.generate_skin_data(client)

    loop = Async_Manager(client=client)
    async_thread = threading.Thread(target=loop.init_loop,daemon=True)
    async_thread.start()

    prompt = Prompt(client=client)
    cli_thread = threading.Thread(target=prompt.main_loop)
    cli_thread.start()
    cli_thread.join()