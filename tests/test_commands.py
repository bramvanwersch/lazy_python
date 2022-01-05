from unittest import TestCase

from lazy_src import commands
import testing_utility


class TestCommand(TestCase):

    def _command_function(self, *args):
        # command function for testing commands
        return 10

    def test_self_command(self):
        test_description = "command for testing"
        command = commands.Command("test", self_command=self._command_function, description=test_description)
        self.assertEqual(10, command())

    def test_add_command(self):
        test_description = "command for testing as well"
        command = commands.Command("test", description=test_description)
        get10_description = "get a 10 man"
        get10_example = "lazy test get10"
        command.add_command("get10", self._command_function, get10_description, get10_example)
        self.assertEqual(10, command("get10"))

    def test_help_self_command(self):
        # test help for command without subcommands
        test_description = "command for testing"
        command = commands.Command("test", self_command=self._command_function, description=test_description)
        print_text = testing_utility.capture_print(command, "help")
        self.assertEqual(print_text, "(lazy)> This is the help message for test. This command has no further "
                                     f"subcommands. The help for this command is:\n(....)> {test_description}\n")

    def test_help_command(self):
        # test help for command with subcommands
        test_description = "command for testing as well"
        command = commands.Command("test", description=test_description)
        get10_description = "get a 10 man"
        get10_example = "lazy test get10"
        command.add_command("get10", self._command_function, get10_description, get10_example)
        print_text = testing_utility.capture_print(command, "help")
        self.assertEqual(print_text, "(lazy)> This is the help message for test. These are the available commands:\n"
                                     f"(....)>  - get10: {get10_description}. Example: '{get10_example}'\n")

    def test_wrong_command(self):
        test_description = "command for testing as well"
        command = commands.Command("test", description=test_description)
        get10_description = "get a 10 man"
        get10_example = "lazy test get10"
        command.add_command("get10", self._command_function, get10_description, get10_example)
        print_text = testing_utility.capture_print(command, "helpme")
        self.assertEqual(print_text, "(lazy)> test expects at least any 1 of these arguments: help, get10\n")
