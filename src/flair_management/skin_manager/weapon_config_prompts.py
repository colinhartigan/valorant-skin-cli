from InquirerPy import prompt, inquirer
from InquirerPy.separator import Separator

from ...flair_management.skin_manager.skin_manager import Skin_Manager

class Prompts:
    @staticmethod
    def select_weapon_type(default="exit", **kwargs):
        skin_data = Skin_Manager.fetch_skin_data()

        type_choices = [
            {"name": "exit", "value": "exit"},
            {"name": "Sidearms", "value": "Sidearm"},
            {"name": "SMGs", "value": "SMG"},
            {"name": "Shotguns", "value": "Shotgun"},
            {"name": "Rifles", "value": "Rifle"},
            {"name": "Sniper Rifles", "value": "Sniper"},
            {"name": "Machine Guns", "value": "Heavy"},
            {"name": "Melee", "value": "Melee"}
        ]
        type_choice = inquirer.select(
            message=f"select a weapon type",
            choices=type_choices,
            pointer=">",
            default=default,
        ).execute()

        if type_choice == "exit":
            return None, None, None, None, None,
        if type_choice == "Melee":
            return Prompts.select_skin(skin_data, "2f59173c-4bed-b6c3-2191-dea9b58be9c7", **kwargs)
        else:
            return Prompts.select_weapon(skin_data, type_choice, **kwargs)

    @staticmethod
    def select_weapon(skin_data, weapon_type, **kwargs):
        weapon_choices = []

        for uuid,data in skin_data.items():
            if data["weapon_type"] == weapon_type:
                enabled_amount = len([skin for skin in data['skins'].keys() if data['skins'][skin]['enabled']])
                if kwargs["weights"]:
                    if enabled_amount > 1:
                        weapon_choices.append({
                            "name": f"{data['display_name']} ({enabled_amount} enabled)",
                            "value": uuid
                        })
                else:
                    weapon_choices.append({
                        "name": f"{data['display_name']} ({len(data['skins'])-1} skins, {enabled_amount} enabled)",
                        "value": uuid
                    })


        weapon_choices.insert(0, {"name": "back", "value": "back"})

        weapon_choice = inquirer.select(
            message=f"[{weapon_type}] select a weapon to view the skins of",
            choices=weapon_choices,
            pointer=">"
        ).execute()

        if weapon_choice == "back":
            return Prompts.select_weapon_type(weapon_type, **kwargs)

        return Prompts.select_skin(skin_data, weapon_choice, **kwargs)

    @staticmethod
    def select_skin(skin_data, weapon_choice, **kwargs):
        tier_aliases = {
            "Deluxe": "DLX",
            "Exclusive": "EXC",
            "Premium": "PRE",
            "Select": "SEL",
            "Ultra": "ULT",
            "Battlepass": "BTP",
            "Standard": "STD"
        }
        weapon_data = skin_data[weapon_choice]

        skins_enabled = len([skin for uuid,skin in weapon_data['skins'].items() if skin['enabled'] and not 'Standard' in skin['display_name']])
        total_skins = len([skin for uuid,skin in weapon_data['skins'].items() if not 'Standard' in skin['display_name']])

        skin_choices = []

        if not kwargs["weights"]:
            skin_choices = [{"name": f"{'√' if data['enabled'] else 'x'} [{tier_aliases[data['tier']['display_name']]}] {data['display_name']} ({len(data['levels'])} levels, {len(data['chromas'])} chromas)", "value": uuid} for uuid, data in weapon_data['skins'].items()]
        else:
            skin_choices = [{"name": f"[{data['weight']}] [{tier_aliases[data['tier']['display_name']]}] {data['display_name']}", "value": uuid} for uuid, data in weapon_data['skins'].items() if data['enabled']]
        
        skin_choices.insert(0, {"name": "back", "value": "back"})

        if kwargs["change_all"]:
            skin_choices.insert(1, {"name": ("disable" if skins_enabled == total_skins else "enable") + " all skins/chromas", "value": "change_all"}) 

        skin_choice = inquirer.select(
            message=f"[{weapon_data['display_name']}] select a skin to modify",
            choices=skin_choices,
            pointer=">"
        ).execute()

        if skin_choice == "back":
            if weapon_data['display_name'] == "Melee":
                return Prompts.select_weapon_type(**kwargs)
            else:
                return Prompts.select_weapon(skin_data, weapon_data['weapon_type'], **kwargs)
        if skin_choice == "change_all":
            kwargs["change_all_method"](weapon_data,skins_enabled == total_skins)
            return Prompts.select_skin(skin_data, weapon_choice, **kwargs)
        else:
            weapon_skin_data = weapon_data['skins'][skin_choice]
            return weapon_data, skin_data, skin_choice, weapon_choice, weapon_skin_data