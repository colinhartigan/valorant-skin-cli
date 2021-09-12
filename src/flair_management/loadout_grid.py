from ..flair_management.skin_manager.skin_manager import Skin_Manager
from ..content.identity_content import Identity_Content
from ..content.skin_content import Skin_Content

class Loadout_Grid:

    @staticmethod
    def fetch_loadout_grid(client,loadout_override=None):
        def ceildiv(a, b):
            return -(-a // b)

        loadout = client.fetch_player_loadout() if loadout_override is None else loadout_override

        loadout_sprays = {
            spray["EquipSlotID"]: spray["SprayID"] for spray in loadout["Sprays"] # should be other way around
        } 

        sprays = Identity_Content.fetch_spray_data()
        buddies = Skin_Content.fetch_gun_buddies()
        inventory = Skin_Manager.fetch_skin_data()

        spray_slot_uuids = {
            "0814b2fe-4512-60a4-5288-1fbdcec6ca48": "Spray1",
            "04af080a-4071-487b-61c0-5b9c0cfaac74": "Spray2", 
            "5863985e-43ac-b05d-cb2d-139e72970014": "Spray3",
        }
        spray_types = {
            "Spray1": "Preround Spray",
            "Spray2": "Midround Spray",
            "Spray3": "Postround Spray",
        }

        loadout_patched = {}

        grid_order = [
            ["Card", "Classic", "Stinger", "Bulldog", "Marshal"],
            ["Title", "Shorty", "Spectre", "Guardian", "Operator"],
            ["Spray1", "Frenzy", "Bucky", "Phantom", "Ares"],
            ["Spray2", "Ghost", "Judge", "Vandal", "Odin"],
            ["Spray3", "Sheriff", None, None, "Melee"],
        ]
        column_tabs = [16,0,0,0,0]
        grid_built = [[] for i in range(20)]

        # determine the important data to store for each item for easy grid building
        for weapon in loadout["Guns"]:
            weapon_data = inventory[weapon["ID"]]
            skin_data = weapon_data["skins"][weapon["SkinID"]]
            level_data = skin_data["levels"][weapon["SkinLevelID"]]
            chroma_data = skin_data["chromas"][weapon["ChromaID"]]
            buddy_data = {"displayName": ""}
            buddy_uuid = weapon["CharmID"] if "CharmID" in weapon.keys() else ""

            for buddy in buddies:
                if buddy["uuid"] == buddy_uuid:
                    buddy_data = buddy

            loadout_patched[weapon_data["display_name"]] = {
                "ID": weapon["ID"],
                "type": "weapon",
                "display_name": skin_data["display_name"],
                "level_name": level_data["display_name"],
                "chroma_name": chroma_data["display_name"],
                "buddy_name": buddy_data["displayName"],
                "color": skin_data["tier"]["color"]
            }

        for slot, uuid in loadout_sprays.items():
            for s in sprays:
                if s["uuid"] == uuid:
                    spray = s
                
            spray_name = spray["displayName"].replace("Spray", "").strip()
            spray_slot = spray_slot_uuids[slot]

            #spray_slot = spray_slot_uuids[loadout_sprays[spray["uuid"]]]
            split = spray_name.split(" ")
            lines = [spray_name,""]
            if len(split) > 2 and len(spray_name) > 16:
                lines[0] = " ".join(split[0:ceildiv(len(split),2)])
                lines[1] = " ".join(i for i in split[ceildiv(len(split),2):])
            loadout_patched[f"{spray_slot}"] = {
                "ID": spray["uuid"],
                "type": "spray",
                "display_name": lines[0],
                "display_name_line2": lines[1],
                "color": "White",
            }

        title_data = Identity_Content.fetch_title_by_id(loadout["Identity"]["PlayerTitleID"])
        title_name = title_data["displayName"].replace("Title","").strip()
        split = title_name.split(" ")
        lines = [title_data["displayName"],""]
        if len(split) > 2 and len(title_data["displayName"]) > 16:
            lines[0] = " ".join(split[0:ceildiv(len(split),2)])
            lines[1] = " ".join(i for i in split[ceildiv(len(split),2):])
        loadout_patched["Title"] = {
            "ID": title_data["uuid"],
            "type": "title",
            "display_name": lines[0],
            "display_name_line2": lines[1],
            "color": "White",
        }

        card_data = Identity_Content.fetch_card_by_id(loadout["Identity"]["PlayerCardID"])
        split = card_data["displayName"].split(" ")
        lines = [card_data["displayName"],""]
        if len(split) > 2 and len(card_data["displayName"]) > 16:
            lines[0] = " ".join(split[0:ceildiv(len(split),2)])
            lines[1] = " ".join(i for i in split[ceildiv(len(split),2):])
            
        loadout_patched["Card"] = {
            "ID": card_data["uuid"],
            "type": "card",
            "display_name": lines[0],
            "display_name_line2": lines[1],
            "color": "White",
        }

        # determine longest string in each column for tab spacing
        for row,items in enumerate(grid_order):
            for column,item_name in enumerate(items):
                if item_name is not None:
                    item_data = loadout_patched[item_name]
                    if len(item_data["display_name"]) > column_tabs[column]:
                        column_tabs[column] = len(item_data["display_name"])
                    if item_data["type"] == "weapon":
                        if len(item_data["level_name"]) > column_tabs[column]:
                            column_tabs[column] = len(item_data["level_name"])
                        if len(item_data["chroma_name"]) > column_tabs[column]:
                            column_tabs[column] = len(item_data["chroma_name"])
                        if len(item_data["buddy_name"]) > column_tabs[column]:
                            column_tabs[column] = len(item_data["buddy_name"])
                    else:
                        if len(item_data["display_name_line2"]) > column_tabs[column]:
                            column_tabs[column] = len(item_data["display_name_line2"])

        # build the actual grid
        row = 0
        width = sum(column_tabs) + (3*len(column_tabs))
        for _,items in enumerate(grid_order):
            for column,item_name in enumerate(items):
                longest = column_tabs[column]+3
                def add_row(start,amt):
                    for i in range(start,start+amt):
                        grid_built[row+i].append(("White","\t".expandtabs(longest)))

                if item_name is not None:
                    
                    if loadout_patched[item_name]["type"] == "weapon": 
                        weapon_data = loadout_patched[item_name]
                        grid_built[row].append((f"{weapon_data['color']} bold",f"{weapon_data['display_name']}\t".expandtabs(longest)))
                        grid_built[row+1].append((f"{weapon_data['color']}",f"{weapon_data['level_name']}\t".expandtabs(longest)))
                        grid_built[row+2].append((f"{weapon_data['color']}",f"{weapon_data['chroma_name']}\t".expandtabs(longest)))
                        grid_built[row+3].append((f"{weapon_data['color']}",f"{weapon_data['buddy_name']}\t".expandtabs(longest)))

                    elif loadout_patched[item_name]["type"] == "title": 
                        title_data = loadout_patched[item_name]
                        grid_built[row].append(("DeepSkyBlue bold",f"Title\t".expandtabs(longest)))
                        grid_built[row+1].append(("White",f"{title_data['display_name']}\t".expandtabs(longest)))
                        grid_built[row+2].append(("White",f"{title_data['display_name_line2']}\t".expandtabs(longest)))
                        add_row(3,1)

                    elif loadout_patched[item_name]["type"] == "card":
                        card_data = loadout_patched[item_name]
                        grid_built[row].append(("DeepSkyBlue bold",f"Card\t".expandtabs(longest)))
                        grid_built[row+1].append(("White",f"{card_data['display_name']}\t".expandtabs(longest)))
                        grid_built[row+2].append(("White",f"{card_data['display_name_line2']}\t".expandtabs(longest)))
                        add_row(3,1)

                    elif "Spray" in item_name:
                        spray_data = loadout_patched[item_name]
                        grid_built[row].append(("DeepSkyBlue bold",f"{spray_types[item_name]}\t".expandtabs(longest)))
                        grid_built[row+1].append(("White",f"{spray_data['display_name']}\t".expandtabs(longest)))
                        grid_built[row+2].append(("White",f"{spray_data['display_name_line2']}\t".expandtabs(longest)))
                        add_row(3,1)

                else:
                    add_row(0,4)
                
            grid_built[row+3].append(("White","\n"))
            row += 4

        return grid_built, width