from ...flair_loader.skin_loader_withcheck import Loader 
from .reload import Reload
from InquirerPy.utils import color_print

class Reset:

    def __init__(self,client):
        color_print([("Green bold", "resetting skin data")])
        Loader.generate_blank_skin_file()
        Loader.generate_skin_data(client)