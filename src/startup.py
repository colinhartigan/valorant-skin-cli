import os, threading, ctypes, time
from valclient.client import Client
from InquirerPy.utils import color_print

from .utility.config_manager import Config
from .utility.onboarding import Onboarder
from .flair_loader.skin_loader_withcheck import Skin_Loader
from .flair_loader.buddy_loader import Buddy_Loader
from .asynchronous.async_manager import Async_Manager
from .cli.command_prompt import Prompt
from .cli.commands.reload import Reload
from .utility.logging import Logger
from .utility.filepath import Filepath
from .utility.version_checker import Checker

kernel32 = ctypes.WinDLL('kernel32')

class Startup:

    @staticmethod
    def run():        
        Startup.check_for_data_folder()
        Startup.setup_inquirer()

        Logger.create_logger()
        Config.check_config()
        config = Config.fetch_config()

        if not config["meta"]["onboarding_completed"]:
            Onboarder()
            # reset the client if region changed during onboarding
            Reload()

        Checker.check_version(config)

        ctypes.windll.kernel32.SetConsoleTitleW(f"valorant-skin-cli {config['version']}") 

        region = config["region"][0].lower()
        client = Client(region=region)
        try:
            client.activate()
        except Exception as e:
            color_print([("Tomato", f"unable to launch: {e}")])
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
            input("press enter to exit...")
            os._exit(1)

        # load skin data
        Skin_Loader.generate_skin_data(client)
        Buddy_Loader.generate_buddy_data(client)
        

        loop = Async_Manager(client=client)
        async_thread = threading.Thread(target=loop.init_loop, daemon=True)
        async_thread.start()

        prompt = Prompt(client=client)
        cli_thread = threading.Thread(target=prompt.main_loop)
        cli_thread.start()
        cli_thread.join()



    @staticmethod
    def setup_inquirer():
        os.environ["INQUIRERPY_NO_RAISE_KBI"] = "true"

    @staticmethod 
    def check_for_data_folder():
        data_path = Filepath.get_appdata_folder()
        if not os.path.isdir(data_path):
            os.makedirs(data_path)