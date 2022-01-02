from typing import Callable

from src import lazy_utility


class Command:
    def __init__(self, name, self_command: Callable = None, description: str = ""):
        self.name = name
        # comand called when no arguments are provided given that it is defined --> this callable can not take args
        self._own_command = self_command
        self._subcommands = {"help": self.print_help}
        self.help_text = description
        self._helps = {}
        self._examples = {}

    def add_command(self, name, function, help_message="", example_usage=""):
        self._subcommands[name] = function
        self._helps[name] = help_message
        self._examples[name] = example_usage

    def print_help(self, *args):
        if len(self._subcommands) == 1:
            lazy_utility.message(f"This is the help message for {self.name}. This command has no further subcommands."
                            f" The help for this command is:\n{self.help_text}")
            return
        full_help_text = f"This is the help message for {self.name}. These are the available commands:\n"
        for key in self._subcommands:
            if key == "help":
                continue
            full_help_text += f" - {key}: {self._helps[key]}. "
            if self._examples[key] != '':
                full_help_text += f"Example: '{self._examples[key]}'\n"
            else:
                full_help_text += "\n"
        lazy_utility.message(full_help_text[:-1])

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            if self._own_command is not None:
                return self._own_command()

            lazy_utility.message(f"{self.name} expects at least 1 argument: Choose one of "
                            f"{', '.join(self._subcommands.keys())}")
            return
        if args[0] not in self._subcommands:
            lazy_utility.message(f"{self.name} expects at least any 1 of these arguments: "
                            f"{', '.join(self._subcommands.keys())}")
            return
        return self._subcommands[args[0]](*args[1:])  # noqa
