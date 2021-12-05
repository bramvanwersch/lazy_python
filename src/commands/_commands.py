from typing import Callable

from src import utility


class Command:
    def __init__(self, name, self_command: Callable = None, description: str = ""):
        self.name = name
        # comand called when no arguments are provided given that it is defined --> this callable can not take args
        self._own_command = self_command
        self._subcommands = {"help": self.print_help}
        self.help_text = description
        self._helps = {}

    def add_command(self, name, function, help_message=""):
        self._subcommands[name] = function
        self._helps[name] = help_message

    def print_help(self, *args):
        if len(self._subcommands) == 1:
            utility.message("This command has no further subcommands. The help for this command is:")
            utility.message(self.help_text)
            return
        utility.message(f"This is the help message for {self.name}. These are the available commands:")
        for key in self._subcommands:
            if key == "help":
                continue
            utility.message(f"\t- {key}: {self._helps[key]}")

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            if self._own_command is not None:
                self._own_command()
                return
            utility.message(f"{self.name} expects at least 1 argument: Choose one of "
                            f"{' ,'.join(self._subcommands.keys())}")
            return
        if args[0] not in self._subcommands:
            utility.message(f"{self.name} expects at least any 1 of these arguments: "
                            f"{' ,'.join(self._subcommands.keys())}")
            return
        self._subcommands[args[0]](*args[1:])  # noqa
