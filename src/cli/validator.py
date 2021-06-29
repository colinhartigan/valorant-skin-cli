from prompt_toolkit.validation import ValidationError, Validator
from .completer_generator import Completer

commands = Completer.generate_completer_dict()

class Command_Validator(Validator):
    def validate(self, document):
        validators = {
            "randomize": lambda result: result.split()[0].strip() in list(commands.keys())
        }
        command = document.text.split()[0]
        args = document.text.split()[1:]
        if not command in list(commands.keys()):
            raise ValidationError(
                message="Invalid command",
                cursor_position=len(document.text)
            )