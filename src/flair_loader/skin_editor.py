from InquirerPy import prompt, inquirer
from InquirerPy.separator import Separator

from .skin_loader import Loader


class Editor:
    '''
    this flows through 4 stages
    weapon type -> weapon -> skins -> skin preferences
    '''

    @staticmethod
    def select_weapon_type():
        skin_data = Loader.fetch_skin_data()

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
            message='[randomizer pool editor] select a weapon type',
            choices=type_choices,
        )
        type_choice = type_choice.execute()

        if type_choice == "exit":
            return
        if type_choice == "Melee":
            Editor.select_skin(skin_data, "2f59173c-4bed-b6c3-2191-dea9b58be9c7")
        else:
            Editor.select_weapon(skin_data, type_choice)

    @staticmethod
    def select_weapon(skin_data, weapon_type):

        weapon_choices = [{
                              "name": f"{data['display_name']} ({len(data['skins'])} skins, {len([skin for skin in data['skins'].keys() if data['skins'][skin]['enabled']])} enabled)",
                              "value": uuid} for uuid, data in skin_data.items() if data['weapon_type'] == weapon_type]
        weapon_choices.insert(0, {"name": "back", "value": "back"})

        weapon_choice = inquirer.select(
            message=f"[{weapon_type}] select a weapon to view the skins of",
            choices=weapon_choices,
        )
        weapon_choice = weapon_choice.execute()

        if weapon_choice == "back":
            Editor.select_weapon_type()
            return

        Editor.select_skin(skin_data, weapon_choice)

    @staticmethod
    def select_skin(skin_data, weapon_choice):
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

        skin_choices = [{
                            "name": f"{'☑' if data['enabled'] else '☒'} [{tier_aliases[data['tier']['display_name']]}] {data['display_name']} ({len(data['levels'])} levels, {len(data['chromas'])} chromas)",
                            "value": uuid} for uuid, data in weapon_data['skins'].items()]
        skin_choices.insert(0, {"name": "back", "value": "back"})

        skin_choice = inquirer.select(
            message=f"[{weapon_data['display_name']}] select a skin to modify",
            choices=skin_choices,
        ).execute()

        if skin_choice == "back":
            if weapon_data['display_name'] == "Melee":
                Editor.select_weapon_type()
            else:
                Editor.select_weapon(skin_data, weapon_data['weapon_type'])
            return

        weapon_skin_data = weapon_data['skins'][skin_choice]
        weapon_data['skins'][skin_choice] = Editor.set_skin_preferences(weapon_skin_data)

        Loader.modify_skin_data(skin_data)
        Editor.select_skin(skin_data, weapon_choice)

    @staticmethod
    def set_skin_preferences(skin_data):
        preferences = [
            {'name': 'skin enabled', 'value': 'skin_enabled', 'enabled': skin_data['enabled']},
            Separator(),
        ]

        # append skin levels
        if len(skin_data['levels']) > 1:
            levels = [{'name': f"[LEVEL] {data['display_name']}", 'value': f"level_{uuid}", 'enabled': data['enabled']}
                      for uuid, data in skin_data['levels'].items()]
            preferences.extend(levels)
            preferences.append(Separator())

        # append chromas
        if len(skin_data['chromas']) > 1:
            chromas = [
                {'name': f"[CHROMA] {data['display_name']}", 'value': f"chroma_{uuid}", 'enabled': data['enabled']} for
                uuid, data in skin_data['chromas'].items()]
            preferences.extend(chromas)

        # preferences prompt
        skin_preferences = inquirer.checkbox(
            message=f"modify skin preferences for {skin_data['display_name']}",
            choices=preferences,
            instruction='(space - toggle, enter - finish)'
        ).execute()

        # clear out all old preferences 
        skin_data['enabled'] = False
        if len(skin_data['levels']) > 1:
            for uuid, level in skin_data['levels'].items():
                level['enabled'] = False
        if len(skin_data['chromas']) > 1:
            for uuid, chroma in skin_data['chromas'].items():
                chroma['enabled'] = False

        # update skin data with new preferences
        for preference in skin_preferences:
            if "level_" in preference or "chroma_" in preference:
                if "level_" in preference:
                    skin_data['levels'][preference.removeprefix('level_')]['enabled'] = True
                if "chroma_" in preference:
                    skin_data['chromas'][preference.removeprefix('chroma_')]['enabled'] = True

            if preference == "skin_enabled":
                skin_data['enabled'] = True

                # check if any have 0 chromas/levels enabled then enable the top level
        enabled_levels = [level for _, level in skin_data['levels'].items() if level['enabled']]
        enabled_chromas = [chroma for _, chroma in skin_data['chromas'].items() if chroma['enabled']]

        if len(enabled_levels) == 0:
            skin_data['levels'][list(skin_data['levels'].keys())[-1]]['enabled'] = True

        if len(enabled_chromas) == 0:
            skin_data['chromas'][list(skin_data['chromas'].keys())[-1]]['enabled'] = True

        return skin_data
