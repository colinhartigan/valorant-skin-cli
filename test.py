from valclient.client import Client
import json

with open("inventory_reference.json") as f:
    inv = json.load(f)
    client = Client()
    client.activate()
    #client.put_player_loadout(inv)

print(json.dumps(client.fetch_player_loadout()))