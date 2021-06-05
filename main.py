from src.commands.command_prompt import Prompt 
from valclient.client import Client

client = Client()
client.hook()

prompt = Prompt(client=client)
prompt.main_loop()