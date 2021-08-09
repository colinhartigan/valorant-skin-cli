from InquirerPy import prompt, inquirer
from InquirerPy.separator import Separator

from ...flair_management.skin_manager.skin_manager import Skin_Manager
from .weapon_config_prompts import Prompts

class Weight_Editor:

    @staticmethod
    def weights_entrypoint():
        weapon_data, skin_data, skin_choice, weapon_choice, weapon_skin_data = Prompts.select_weapon_type(change_all=False, weights=True)

        while weapon_data is not None:
            weapon_data['skins'][skin_choice]["weight"] = Weight_Editor.set_weight(weapon_skin_data)
            Skin_Manager.modify_skin_data(skin_data)

            weapon_data, skin_data, skin_choice, weapon_choice, weapon_skin_data = Prompts.select_skin(skin_data, weapon_choice, change_all=False, weights=True)

    def set_weight(skin_data):
        current_weight = str(skin_data["weight"])
        new_weight = inquirer.text(
            message=f"[{skin_data['display_name']}] enter randomizer weight (currently {current_weight})",
            default=current_weight,
            validate=lambda result: result.isdigit(),
            filter=lambda result: int(result)
        ).execute()
        
        return new_weight