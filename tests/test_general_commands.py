from unittest import TestCase
import random

from src.commands import general_commands
from src.commands import train
from src import lazy_constants
import testing_setup
import testing_utility


class Test(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_check_normal(self):
        random.seed(1)
        # check without
        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n")
        train.gather()  # because testing will go for 3600 seconds
        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old_bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "exploring:0\ngathering:4\nwoodcutting:0\nfishing:0\n")

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "old_bread:2\ncoin:4\n")

        # repeat the gathering to ensure that values are properly added and not overwritten --> because we are testing
        # this can be done by rechecking

        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +3xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 3 X coin{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found old_bread{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "exploring:0\ngathering:7\nwoodcutting:0\nfishing:0\n")

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "old_bread:3\ncoin:7\n")

        # NOTE: there is no real way to asser that the time stamp is written

    def test_check_explore(self):
        # because exploring is handled differntly
        random.seed(1)
        # check without
        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n")
        train.explore()  # because testing will go for 3600 seconds
        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +300xp (0-15){lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered small_lake{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_tree{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "exploring:300\ngathering:0\nwoodcutting:0\nfishing:0\n")

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "")

        # repeat the gathering to ensure that values are properly added and not overwritten --> because we are testing
        # this can be done by rechecking

        output = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +120xp (15-17){lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "exploring:420\ngathering:0\nwoodcutting:0\nfishing:0\n")

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "")

    def test_examine_area(self):
        self.fail()

    def test_examine_location(self):
        self.fail()

    def test_examine_activity(self):
        self.fail()

    def test__examine(self):
        self.fail()

    def test__get_area(self):
        self.fail()

    def test__get_location(self):
        self.fail()

    def test__get_activity(self):
        self.fail()

    def test_move_area(self):
        self.fail()

    def test_move_location(self):
        self.fail()

    def test__move(self):
        self.fail()

    def test__update(self):
        self.fail()
