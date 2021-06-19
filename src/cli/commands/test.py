from termcolor import cprint

class Test:

    def __init__(self,client):
        self.client = client
        entitlements = self.client.fetch_store_entitlements("3ad1b2b2-acdb-4524-852f-954a76ddae0a")