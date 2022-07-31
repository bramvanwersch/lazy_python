from unittest import TestCase
import random
import re

from lazy_src.commands import general_commands
from lazy_src.commands import train
from lazy_src import lazy_constants
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
        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n")
        train.gather()  # because testing will go for 3600 seconds
        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        for line in text:
            if line.startswith("gathering"):
                self.assertEqual(line, "gathering:4\n")
                break

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "old bread:2\ncoin:4\n")

        # repeat the gathering to ensure that values are properly added and not overwritten --> because we are testing
        # this can be done by rechecking

        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +3xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 3 X coin{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found old bread{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        for line in text:
            if line.startswith("gathering"):
                self.assertEqual(line, "gathering:7\n")
                break

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "old bread:3\ncoin:7\n")

        # NOTE: there is no real way to assert that the time stamp is written

    def test_check_explore(self):
        # because exploring is handled differntly
        random.seed(1)
        # check without
        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n")
        train.explore()  # because testing will go for 3600 seconds
        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +330xp (0-15){lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_quarry{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_tree{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered small_lake{lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        for line in text:
            if line.startswith("exploring"):
                self.assertEqual(line, "exploring:300\n")
                break

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "")

        # repeat the gathering to ensure that values are properly added and not overwritten --> because we are testing
        # this can be done by rechecking

        output, _ = testing_utility.capture_print(general_commands.check)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +120xp (15-18){lazy_constants.RESET_COLOR}\n")
        # check items and levels being written properly
        with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            text = f.read()
        for line in text:
            if line.startswith("exploring"):
                self.assertEqual(line, "exploring:420\n")
                break

        with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            text = f.read()
        self.assertEqual(text, "")

    def test_examine_area(self):
        # check normal
        output, _ = testing_utility.capture_print(general_commands.examine_area, "green_woods")
        self.assertEqual(output, "(lazy)> GREEN_WOODS:\n"
                                 "(....)> The starting are. The place I grew up in and call home.\n"
                                 "(....)> Locations:\n"
                                 "(....)> - ???: ???\n"
                                 "(....)> - ???: ???\n"
                                 "(....)> - home: A place with good and bad memories\n"
                                 "(....)> - ???: ???\n")

    def test_examine_area_wrong_name(self):
        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woodse:r")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No area with name green_woodse:r."
                                 f"{lazy_constants.RESET_COLOR}\n")

    def test_examine_location(self):
        # check normal
        output, _ = testing_utility.capture_print(general_commands.examine_location, "green_woods", "home")
        self.assertEqual(output, "(lazy)> HOME:\n"
                                 "(....)> A place with good and bad memories\n"
                                 "(....)> Activities:\n"
                                 "(....)>  - gathering (min. lvl. 0 gathering): There might be some supplies left,"
                                 " on the other hand there is a reason im leaving.\n")

    def test_examine_location_wrong_name(self):
        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woodse:r")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No area with name green_woodse:r."
                                 f"{lazy_constants.RESET_COLOR}\n")

        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woods", "home:r")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No location with name home:r."
                                 f"{lazy_constants.RESET_COLOR}\n")

    def test_examine_activity(self):
        # check normal
        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woods", "home", "gathering")
        self.assertEqual(output, "(lazy)> GATHERING:\n"
                                 "(....)> There might be some supplies left, on the other hand there is a "
                                 "reason im leaving.\n"
                                 "(....)> Available loot:\n"
                                 "(....)>  - coin: 1\n"
                                 "(....)>  - old bread: 1\n"
                                 "(....)>  - small dagger: 1\n"
                                 "(....)>  - black cape: 1\n"
                                 "(....)>  - leather boots: 1\n")

    def test_examine_activity_wrong_name(self):
        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woodse:r")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No area with name green_woodse:r."
                                 f"{lazy_constants.RESET_COLOR}\n")

        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woods", "home:r")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No location with name home:r."
                                 f"{lazy_constants.RESET_COLOR}\n")

        output, _ = testing_utility.capture_print(general_commands.examine_activity, "green_woods", "home", "gather:")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No activity with name gather:."
                                 f"{lazy_constants.RESET_COLOR}\n")

    def test_examine_item(self):
        output, _ = testing_utility.capture_print(general_commands.examine_items, "log")
        self.assertEqual(output, "(lazy)> log: This can be used for all sorts of things\n")

    def test_examine_item_wrong_name(self):
        output, _ = testing_utility.capture_print(general_commands.examine_items, "logger")

        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No item with name 'logger' "
                                 f"exists.{lazy_constants.RESET_COLOR}\n")

    def test_move_area(self):
        # NOTE: not checked if area is actually written to file, only one area available at the moment
        random.seed(1)
        train.gather()  # make sure this value is set to check it is reset

        output, _ = testing_utility.capture_print(general_commands.move_area, "green_woods")
        self.assertEqual(output,
                         "(lazy)> Before moving the current activity is checked:\n"
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n"
                         "(....)> \n"
                         "(lazy)> You moved to area green_woods. You are ready to go do something...\n")

        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_GENERAL_FILE_NAME) as f:
            text = f.read()
        activity_text = re.findall(f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:.*", text)
        self.assertTrue(len(activity_text) == 1)
        self.assertEqual(activity_text[0], f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:")

        train.gather()  # make sure that the value is not reset on fail
        output, _ = testing_utility.capture_print(general_commands.move_area, "green_woods:")
        self.assertEqual(output,
                         "(lazy)> Before moving the current activity is checked:\n"
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +3xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 3 X coin{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found old bread{lazy_constants.RESET_COLOR}\n"
                         "(....)> \n"
                         f"(lazy)> {lazy_constants.WARNING_COLOR}No area with name green_woods:."
                         f"{lazy_constants.RESET_COLOR}\n")

        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_GENERAL_FILE_NAME) as f:
            text = f.read()
        activity_text = re.findall(f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:.*", text)
        self.assertTrue(len(activity_text) == 1)
        self.assertEqual(activity_text[0], f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:gathering")

    def test_move_location(self):
        # NOTE: not checked if area is actually written to file, only one area available at the moment
        random.seed(1)
        train.gather()  # make sure this value is set to check it is reset

        output, _ = testing_utility.capture_print(general_commands.move_location, "green_woods", "home")
        self.assertEqual(output,
                         "(lazy)> Before moving the current activity is checked:\n"
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n"
                         "(....)> \n"
                         "(lazy)> You moved to location home. You are ready to go do something...\n")

        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_GENERAL_FILE_NAME) as f:
            text = f.read()
        activity_text = re.findall(f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:.*", text)
        self.assertTrue(len(activity_text) == 1)
        self.assertEqual(activity_text[0], f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:")

        train.gather()  # make sure that the value is not reset on fail
        output, _ = testing_utility.capture_print(general_commands.move_location, "green_woods", "homer:")
        self.assertEqual(output,
                         "(lazy)> Before moving the current activity is checked:\n"
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +3xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 3 X coin{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found old bread{lazy_constants.RESET_COLOR}\n"
                         "(....)> \n"
                         f"(lazy)> {lazy_constants.WARNING_COLOR}No location with name homer:."
                         f"{lazy_constants.RESET_COLOR}\n")

        user_dir = lazy_constants.USER_DIRS_PATH / "test"
        with open(user_dir / lazy_constants.USER_GENERAL_FILE_NAME) as f:
            text = f.read()
        activity_text = re.findall(f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:.*", text)
        self.assertTrue(len(activity_text) == 1)
        self.assertEqual(activity_text[0], f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:gathering")

    def test_update(self):
        # has to be extended and is kind of hard to test properly/consistently
        pass
