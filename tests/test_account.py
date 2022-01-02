from unittest import TestCase
from pathlib import Path

from src.commands import account
import testing_setup
import testing_utility
from src import lazy_constants


class Test(TestCase):

    def setUp(self) -> None:
        testing_setup.setup_test_folder()

    def tearDown(self) -> None:
        testing_setup.remove_test_folder()

    def test_new(self):
        # inputs are not checked
        username = "test"
        password = "test"
        account.new(username, password, password)
        # check all created files
        user_file_dir = lazy_constants.USER_DIRS_PATH / username
        try:
            with open(user_file_dir / "general.txt") as f:
                text = f.read()
            self.assertTrue(text.startswith("current_area:green_woods\ncurrent_location:home\ncurrent_activity:\n"
                                            "last_time_stamp:"))  # timestamp not included will continusly change ofc
        except IOError:
            self.fail("general.txt file is missing on new account creation")

        try:
            with open(user_file_dir / "inventory.txt") as f:
                text = f.read()
            self.assertEqual(text, '')
        except IOError:
            self.fail("inventory.txt file is missing on new account creation")

        try:
            with open(user_file_dir / "levels.txt") as f:
                text = f.read()
            self.assertEqual(text, 'exploring:0\ngathering:0\nwoodcutting:0\nfishing:0\n')
        except IOError:
            self.fail("levels.txt file is missing on new account creation")

        if not Path(user_file_dir / "areas").exists():
            self.fail("Area dir was not created on new account creation")

        try:
            with open(user_file_dir / "areas" / lazy_constants.STARTING_AREA) as f:
                text = f.read()
            self.assertEqual(text, f'unlocked_locations:{lazy_constants.STARTING_LOCATION}\n')
        except IOError:
            self.fail("starting area file is missing on new account creation")

    def test_activate(self):
        username = "test"
        password = "test"
        account.new(username, password, password)
        username = "test2"
        password = "test2"
        account.new(username, password, password)
        account.activate("test", "test")
        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:test\n")

        account.activate("test2", "test2")
        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:test2\n")

        # make sure mistakes are pointed out
        output = testing_utility.capture_print(account.activate, "test", "test2")
        print(output)
        output = testing_utility.capture_print(account.activate, "test3", "test2")
        print(output)

    # def test_info(self):
    #     self.fail()
    #
    # def test__show_general_information(self):
    #     self.fail()
    #
    # def test__show_levels(self):
    #     self.fail()
    #
    # def test__show_inventory(self):
    #     self.fail()
    #
    # def test_delete(self):
    #     self.fail()
    #
    # def test__get_username_password(self):
    #     self.fail()
    #
    # def test__confirm_password(self):
    #     self.fail()
