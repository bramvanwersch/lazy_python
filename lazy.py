# lirbrary imports
from sys import argv

# own imports
from lazy_src import commands
from lazy_src import lazy_utility


def main():
    arguments = argv[1:]
    if len(arguments) == 0:
        lazy_utility.message(f"Please provide one of the possible commands: {', '.join(commands.COMMANDS.keys())}, help")
        return -1
    else:
        main_command = arguments[0]
        if main_command == "help":
            show_main_help()
            return 0
        if main_command not in commands.COMMANDS:
            lazy_utility.message(f"Please provide one of the possible commands: {', '.join(commands.COMMANDS.keys())}")
            return -1
        return commands.COMMANDS[main_command](*arguments[1:])


def show_main_help():
    lazy_utility.message("Welcome to lazy. This program is used with the help of a number of commands. Here is a "
                         "list of all the possible commands and a small explanation. Each command has additional help "
                         "information by typing the command followed by help.")
    for index, (command_name, command) in enumerate(commands.COMMANDS.items()):
        if command_name == "help":
            continue
        if index == 0:
            continue_last = False
        else:
            continue_last = True
        lazy_utility.message(f" - {command_name}: {command.help_text}", continue_last=continue_last)


if __name__ == '__main__':
    main()
