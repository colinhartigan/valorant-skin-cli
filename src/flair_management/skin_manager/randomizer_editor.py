from InquirerPy import prompt, inquirer
from InquirerPy.separator import Separator

from ...flair_management.skin_manager.skin_manager import Skin_Manager
from .weapon_config_prompts import Prompts


class Randomizer_Editor:
    '''
    this flows through 4 stages
    weapon type -> weapon -> skins -> skin preferences
    '''

    @staticmethod
    def randomizer_entrypoint():
        weapon_data, skin_data, skin_choice, weapon_choice, weapon_skin_data = Prompts.select_weapon_type(change_all=True,weights=False)
        while weapon_data is not None:
            weapon_data['skins'][skin_choice] = Randomizer_Editor.set_skin_preferences(weapon_skin_data)
            Skin_Manager.modify_skin_data(skin_data)
            weapon_data, skin_data, skin_choice, weapon_choice, weapon_skin_data = Prompts.select_skin(skin_data, weapon_choice, change_all=True, weights=False)    


    @staticmethod
    def change_all_skins_by_weapon(weapon_data,disable):
        for uuid, skin in weapon_data["skins"].items():
            if not "Standard" in skin["display_name"]:
                skin["enabled"] = not disable
                # disable all levels except for max level
                for uuid, level in skin["levels"].items():
                    level["enabled"] = False
                skin['levels'][list(skin['levels'].keys())[-1]]['enabled'] = True

                for uuid, chroma in skin["chromas"].items():
                    chroma["enabled"] = not disable
            
            # make sure theres still at least 1 chroma enabled (on disable)
            enabled_chromas = [chroma for _, chroma in skin['chromas'].items() if chroma['enabled']]
            if len(enabled_chromas) == 0:
                skin['chromas'][list(skin['chromas'].keys())[-1]]['enabled'] = True

    @staticmethod
    def set_skin_preferences(skin_data):
        preferences = [
            {'name': 'skin enabled', 'value': 'skin_enabled',
                'enabled': skin_data['enabled']},
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
            instruction='(space - toggle, enter - finish)',
            pointer='>',
            enabled_symbol='√ ',
            disabled_symbol='x '
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
                    skin_data['levels'][preference[len('level_'):]]['enabled'] = True
                if "chroma_" in preference:
                    skin_data['chromas'][preference[len('chroma_'):]]['enabled'] = True

            if preference == "skin_enabled":
                skin_data['enabled'] = True

        # check if any have 0 chromas/levels enabled then enable the top level
        enabled_levels = [
            level for _, level in skin_data['levels'].items() if level['enabled']]
        enabled_chromas = [
            chroma for _, chroma in skin_data['chromas'].items() if chroma['enabled']]

        if len(enabled_levels) == 0:
            skin_data['levels'][list(
                skin_data['levels'].keys())[-1]]['enabled'] = True

        if len(enabled_chromas) == 0:
            skin_data['chromas'][list(
                skin_data['chromas'].keys())[-1]]['enabled'] = True

        return skin_data