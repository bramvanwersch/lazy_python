from src import utility


class Command:
    def __init__(self, name):
        self.name = name
        self._subcommands = {"help": self.print_help}
        self._helps = {}

    def add_command(self, name, function, help_message=""):
        self._subcommands[name] = function
        self._helps[name] = help_message

    def print_help(self):
        utility.message(f"This is the help message for {self.name}. These are the available commands:")
        for key in self._subcommands:
            utility.message(f"\t- {key}: {self._helps[key]}")

    def __call__(self, *args, **kwargs):
        if len(args) == 0:
            utility.message(f"{self.name} expects at least 1 argument: Choose one of "
                            f"{' ,'.join(self._subcommands.keys())}")
            return
        if args[0] not in self._subcommands:
            utility.message(f"{self.name} expects at any 1 of these arguments: {' ,'.join(self._subcommands.keys())}")
            return
        self._subcommands[args[0]]()
