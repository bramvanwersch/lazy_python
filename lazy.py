# lirbrary imports
from sys import argv

# own imports
from src.account import ACCOUNT_COMMANDS
from src import utility


_COMMANDS = {
    "account": ACCOUNT_COMMANDS
}


def main():
    arguments = argv[1:]
    if len(arguments) == 0:
        utility.message(f"Please provide one of the possible commands: {' ,'.join(_COMMANDS.keys())}")
        return -1
    else:
        main_command = arguments[0]
        if main_command not in _COMMANDS:
            utility.message(f"Please provide one of the possible commands: {' ,'.join(_COMMANDS.keys())}")
            return -1
        _COMMANDS[main_command](*arguments[1:])
    return 0


if __name__ == '__main__':
    main()
