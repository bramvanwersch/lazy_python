from unittest import TestCase
from pathlib import Path

from lazy_src.commands import account
import testing_setup
import testing_utility
from lazy_src import lazy_constants


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
            self.assertEqual(text, 'exploring:0\ngathering:0\nwoodcutting:0\nfishing:0\nmining:0\nstealing:0\nfarming:0'
                                   '\narcheology:0\nhunting:0\nranging:0\nfighting:0\nspellcasting:0\nworshipping:0\n'
                                   'leatherworking:0\nfletching:0\nweaving:0\narmor_smithing:0\nweapon_smithing:0\n'
                                   'brewing:0\nbuilding:0\ncooking:0\nwriting:0\n')
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

        self.assertTrue(Path(user_file_dir / lazy_constants.USER_PEOPLE_DIR).exists())

        # test double account name
        output, _ = testing_utility.capture_print(account.new, "test")
        self.assertTrue(output.startswith(f"(lazy)> {lazy_constants.WARNING_COLOR}Username 'test' is already in use."))

        # test invalid character name
        output, _ = testing_utility.capture_print(account.new, "test:")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '
                                 f'contains at least 1 character and does not contain the following charaters:'
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

        # test wrong repeated password
        output, _ = testing_utility.capture_print(account.new, "test3", "test3", "test4")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Given and repeated password do not match.'
                                 f'{lazy_constants.RESET_COLOR}\n')

        # test invalid character in password
        output, _ = testing_utility.capture_print(account.new, "test3", "test:3", "test:3")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '
                                 f'contains at least 1 character and does not contain the following charaters:'
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

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

        # check invalid username
        output, _ = testing_utility.capture_print(account.activate, "test3", "test2")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Account with username 'test3' does not exist."
                                 f"{lazy_constants.RESET_COLOR}\n")

        # check invalid password
        output, _ = testing_utility.capture_print(account.activate, "test", "test2")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Password does not match the password for "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_info(self):
        username = "test"
        password = "test"
        account.new(username, password, password)

        # check no active account
        output, _ = testing_utility.capture_print(account.info, "levels")
        self.assertEqual(output, "(lazy)> The current active account is: No active account\n")

        account.activate("test", "test")
        # check with active account
        output, _ = testing_utility.capture_print(account.info)
        self.assertTrue(output.startswith("(lazy)> The current active account is: test\n(....)> This account is located"
                                          " in area green_woods at location home Your last activity check was"))

        # check for levels
        output, _ = testing_utility.capture_print(account.info, "levels")
        self.assertEqual(output, "(lazy)> The current active account is: test\n"
                                 "(....)> Levels:\n(....)> exploring: 0 (10 until next)\n"
                                 "(....)> gathering: 0 (10 until next)\n(....)> woodcutting: 0 (10 until next)\n"
                                 "(....)> fishing: 0 (10 until next)\n"
                                 "(....)> mining: 0 (10 until next)\n"
                                 "(....)> stealing: 0 (10 until next)\n"
                                 "(....)> farming: 0 (10 until next)\n"
                                 "(....)> archeology: 0 (10 until next)\n"
                                 "(....)> hunting: 0 (10 until next)\n"
                                 "(....)> ranging: 0 (10 until next)\n"
                                 "(....)> fighting: 0 (10 until next)\n"
                                 "(....)> spellcasting: 0 (10 until next)\n"
                                 "(....)> worshipping: 0 (10 until next)\n"
                                 "(....)> leatherworking: 0 (10 until next)\n"
                                 "(....)> fletching: 0 (10 until next)\n"
                                 "(....)> weaving: 0 (10 until next)\n"
                                 "(....)> armor_smithing: 0 (10 until next)\n"
                                 "(....)> weapon_smithing: 0 (10 until next)\n"
                                 "(....)> brewing: 0 (10 until next)\n"
                                 "(....)> building: 0 (10 until next)\n"
                                 "(....)> cooking: 0 (10 until next)\n"
                                 "(....)> writing: 0 (10 until next)\n")

        # check for items
        output, _ = testing_utility.capture_print(account.info, "items")
        self.assertEqual(output, "(lazy)> The current active account is: test\n")  # no items yet in inventory

        # check for no valid information provided
        output, _ = testing_utility.capture_print(account.info, "invalid argument")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid option provided for lazy account info."
                                 f" Expected on of: levels, items.{lazy_constants.RESET_COLOR}\n")

    def test_delete(self):
        username = "test"
        password = "test"
        account.new(username, password, password)

        # delete with no account selected
        output, _ = testing_utility.capture_print(account.delete)
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No user selected. Select a user with 'account "
                                 f"activate' or create a new one with 'account new'.{lazy_constants.RESET_COLOR}\n")

        # delete with wrong password
        account.activate(username, password)
        output, _ = testing_utility.capture_print(account.delete, "test1")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Password does not match the password for "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

        # invalid character in password
        output, _ = testing_utility.capture_print(account.delete, "test:")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '
                                 f'contains at least 1 character and does not contain the following charaters:'
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

        # delete account check files
        account.delete("test")

        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:\n")

        if Path(lazy_constants.USER_DIRS_PATH / "test").exists():
            self.fail("Account was not properly deleted upon calling delete")

    def test_get_username_password(self):
        name, pw = account._get_username_password("test")
        self.assertEqual(name, None)
        self.assertEqual(pw, None)

        username = "test"
        password = "pw_test"
        account.new(username, password, password)

        name, pw = account._get_username_password("test")
        self.assertEqual(name, "test")
        self.assertEqual(pw, "pw_test")
