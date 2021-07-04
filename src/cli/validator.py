from prompt_toolkit.validation import ValidationError, Validator
from .completer_generator import Completer


class Command_Validator(Validator):

    @staticmethod
    def validate(document):
        commands = Completer.generate_completer_dict()
        command = document.text.split()[0].strip()
        args = document.text.split()[1:]
        if command not in list(commands.keys()):
            # validator for regular commands
            raise ValidationError(
                message="Invalid command",
                cursor_position=len(document.text)
            )
        else:

            # validator overrides for more complex commands
            if command == "set":
                # check if set command has required arguments which match expected inputs
                completer_data = commands["set"]
                if len(args) < 2:
                    raise ValidationError(
                        message="Missing required arguments",
                        cursor_position=len(document.text)
                    )
                valid = False

                # who knew something so simple could make my life so easy
                next_data = completer_data
                for index in range(0, len(args)):
                    if args[index] in next_data.keys():
                        next_data = next_data[args[index]]
                        valid = True
                    else:
                        valid = False
                if valid:
                    return True

                raise ValidationError(
                    message="Syntax error, ensure you entered a valid weapon/skin",
                    cursor_position=len(document.text)
                )
