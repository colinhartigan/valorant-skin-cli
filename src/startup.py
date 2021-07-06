import os
import sys
from valclient.client import Client
import threading
from InquirerPy.utils import color_print

from .utility.config_manager import Config
from .utility.onboarding import Onboarder
from .flair_loader.skin_loader import Loader
from .asynchronous.async_manager import Async_Manager
from .cli.command_prompt import Prompt
from .utility.logging import Logger
from .utility.filepath import Filepath


class Startup:

    @staticmethod
    def run():        
        Startup.check_for_data_folder()
        Startup.setup_inquirer()

        Logger.create_logger()
        config = Config.fetch_config()

        region = config["region"].lower()
        client = Client(region=region)
        try:
            client.hook()
        except Exception as e:
            color_print([("Tomato", f"unable to launch: {e}")])
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