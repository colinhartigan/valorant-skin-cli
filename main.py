from src.skin_manager.command_prompt import Prompt 
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.



if os.environ.get("USERNAME") != "":
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    Prompt({'username':username,'password':password})
else:
    Prompt()