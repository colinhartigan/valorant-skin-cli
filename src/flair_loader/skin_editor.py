import json 
import os
from termcolor import cprint,colored

from InquirerPy import prompt,inquirer
from InquirerPy.separator import Separator

from .skin_loader import Loader

class Editor:

    @staticmethod
    def select_weapon():
        skin_data = Loader.fetch_skin_data()

        weapon_count = len(skin_data.keys())

        weapon_choices = [{"name":f"{data['display_name']} ({len(data['skins'])} skins, {len([skin for skin in data['skins'].keys() if data['skins'][skin]['enabled']])} enabled)","value":uuid} for uuid,data in skin_data.items()]
        weapon_choices.insert(0,{"name":"exit","value":"exit"})

        weapon_choice = inquirer.select( 
            message = 'select a weapon to view the skins of',
            choices = weapon_choices,
            height = "100%",
        )
        weapon_choice = weapon_choice.execute()

        if weapon_choice == "exit":
            return
        
        Editor.select_skin(skin_data,weapon_choice)


    @staticmethod 
    def select_skin(skin_data,weapon_choice):

        weapon_data = skin_data[weapon_choice]

        skin_choices = [{"name":f"{'☑' if data['enabled'] else '☒'} {data['display_name']} ({len(data['levels'])} levels, {len(data['chromas'])} chromas)","value":uuid} for uuid,data in weapon_data['skins'].items()]
        skin_choices.insert(0,{"name":"back","value":"back"})

        skin_choice = inquirer.select(
            message = 'select a skin to modify',
            choices = skin_choices,
            height = "100%",
        ).execute()

        if skin_choice == "back":
            Editor.select_weapon()
            return

        weapon_skin_data = weapon_data['skins'][skin_choice]
        weapon_data['skins'][skin_choice] = Editor.set_skin_preferences(weapon_skin_data)

        Loader.modify_skin_data(skin_data)
        Editor.select_skin(skin_data,weapon_choice)


    @staticmethod
    def set_skin_preferences(skin_data):
        preferences = [
            {'name': 'skin enabled', 'value': 'skin_enabled', 'enabled': skin_data['enabled']},
            Separator(),
        ]

        # append skin levels
        if len(skin_data['levels']) > 1:
            levels = [{'name': f"[LEVEL] {data['display_name']}", 'value': f"level_{uuid}", 'enabled': data['enabled']} for uuid,data in skin_data['levels'].items()]
            preferences.extend(levels)
            preferences.append(Separator())

        # append chromas
        if len(skin_data['chromas']) > 1:
            chromas = [{'name': f"[CHROMA] {data['display_name']}", 'value': f"chroma_{uuid}", 'enabled': data['enabled']} for uuid,data in skin_data['chromas'].items()]
            preferences.extend(chromas)
        
        # preferences prompt
        skin_preferences = inquirer.checkbox(
            message = f"modify skin preferences for {skin_data['display_name']}",
            choices = preferences,
            height = "100%",
            instruction = '(space - toggle, enter - finish)'
        ).execute()

        # clear out all old preferences 
        skin_data['enabled'] = False 
        if len(skin_data['levels']) > 1:
            for uuid,level in skin_data['levels'].items():
                level['enabled'] = False 
        if len(skin_data['chromas']) > 1:
            for uuid,chroma in skin_data['chromas'].items():
                chroma['enabled'] = False

        # update skin data with new preferences
        for preference in skin_preferences:
            if "level_" in preference or "chroma_" in preference:
                if "level_" in preference:
                    skin_data['levels'][preference.removeprefix('level_')]['enabled'] = True
                if "chroma_" in preference:
                    skin_data['chromas'][preference.removeprefix('chroma_')]['enabled'] = True

            if preference == "skin_enabled":
                print('enable')
                skin_data['enabled'] = True 

        return skin_data