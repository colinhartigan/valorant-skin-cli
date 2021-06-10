from src.cli.command_prompt import Prompt 
from src.async_manager.async_manager import Async_Manager

from valclient.client import Client
import threading


if __name__ == "__main__":
    client = Client()
    client.hook()

    prompt = Prompt(client=client)
    cli_thread = threading.Thread(target=prompt.main_loop)
    cli_thread.start()

    loop = Async_Manager(client=client)
    async_thread = threading.Thread(target=loop.init_loop)
    async_thread.start()