from unittest import TestCase
from pathlib import Path

from lazy_src.commands import account
import testing_setup
import testing_utility
from lazy_src import lazy_constants
from lazy_src import items


class TestAccount(TestCase):

    def setUp(self) -> None:
        testing_setup.setup_test_folder()

    def tearDown(self) -> None:
        testing_setup.remove_test_folder()

    def test_new_files_created(self):
        # inputs are not checked
        testing_setup.create_test_account(activate=False)
        # check all created files
        user_file_dir = lazy_constants.USER_DIRS_PATH / "test"
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
            self.assertEqual(text, """exploring:0
gathering:0
woodcutting:0
fishing:0
mining:0
stealing:0
farming:0
archeology:0
hunting:0
ranging:0
fighting:0
spellcasting:0
worshipping:0
leatherworking:0
fletching:0
weaving:0
armor_smithing:0
weapon_smithing:0
brewing:0
building:0
cooking:0
writing:0
""")
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

        try:
            with open(user_file_dir / lazy_constants.USER_EQUIPMENT_FILE_NAME) as f:
                text = f.read()
            expected_text = ''.join(f"{slot}:\n" for slot in items.WearableItem.all_equipment_slots())
            self.assertEqual(text, expected_text)
        except IOError:
            self.fail("equipment file is missing on new account creation")

    def test_new_double_account_name(self):
        testing_setup.create_test_account(activate=False)
        output, _ = testing_utility.capture_print(account.new, "test")
        self.assertTrue(output.startswith(f"(lazy)> {lazy_constants.WARNING_COLOR}Username 'test' is already in use."))

    def test_new_invalid_character_name(self):
        output, _ = testing_utility.capture_print(account.new, "test:")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '  # noqa
                                 f'contains at least 1 character and does not contain the following charaters:'
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

    def test_new_wrong_repeated_password(self):
        output, _ = testing_utility.capture_print(account.new, "test3", "test3", "test4")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Given and repeated password do not match.'
                                 f'{lazy_constants.RESET_COLOR}\n')

    def test_new_invalid_character_password(self):
        output, _ = testing_utility.capture_print(account.new, "test3", "test:3", "test:3")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '
                                 f'contains at least 1 character and does not contain the following charaters:'  # noqa
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

    def test_activate(self):
        testing_setup.create_test_account()
        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:test\n")

    def test_activate_switch(self):
        testing_setup.create_test_account()
        account.new("test2", "test2", "test2")
        account.activate("test2", "test2")
        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:test2\n")

    def test_activate_fail_username(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.activate, "test3", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Account with username 'test3' does not exist."
                                 f"{lazy_constants.RESET_COLOR}\n")

    def test_activate_fail_password(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.activate, "test", "test2")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Password does not match the password for "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_info_no_active_account(self):
        testing_setup.create_test_account(activate=False)

        output, _ = testing_utility.capture_print(account.info, "levels")
        self.assertEqual(output, "(lazy)> The current active account is: No active account\n")

    def test_info_active_account(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.info)
        self.assertTrue(output.startswith("(lazy)> The current active account is: test\n(....)> This account is located"
                                          " in area green_woods at location home Your last activity check was"))

    def test_info_active_account_levels(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.info, "levels")
        expected_output = """(lazy)> The current active account is: test
(....)> Levels:
(....)> exploring: 0 (10 until next)
(....)> gathering: 0 (10 until next)
(....)> woodcutting: 0 (10 until next)
(....)> fishing: 0 (10 until next)
(....)> mining: 0 (10 until next)
(....)> stealing: 0 (10 until next)
(....)> farming: 0 (10 until next)
(....)> archeology: 0 (10 until next)
(....)> hunting: 0 (10 until next)
(....)> ranging: 0 (10 until next)
(....)> fighting: 0 (10 until next)
(....)> spellcasting: 0 (10 until next)
(....)> worshipping: 0 (10 until next)
(....)> leatherworking: 0 (10 until next)
(....)> fletching: 0 (10 until next)
(....)> weaving: 0 (10 until next)
(....)> armor_smithing: 0 (10 until next)
(....)> weapon_smithing: 0 (10 until next)
(....)> brewing: 0 (10 until next)
(....)> building: 0 (10 until next)
(....)> cooking: 0 (10 until next)
(....)> writing: 0 (10 until next)
"""
        self.assertSetEqual(set(output.split("\n")), set(expected_output.split("\n")))

    def test_info_active_account_items(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.info, "items")
        self.assertEqual(output, "(lazy)> The current active account is: test\n")  # no items yet in inventory

    def test_info_active_account_fail(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.info, "invalid argument")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid option provided for lazy account info."
                                 f" Expected on of: levels, items.{lazy_constants.RESET_COLOR}\n")

    def test_delete_no_selected(self):
        testing_setup.create_test_account(activate=False)
        # delete with no account selected
        output, _ = testing_utility.capture_print(account.delete)
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No user selected. Select a user with 'account "
                                 f"activate' or create a new one with 'account new'.{lazy_constants.RESET_COLOR}\n")

    def test_delete_wrong_password(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.delete, "test1")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Password does not match the password for "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_delete_invalid_character(self):
        testing_setup.create_test_account()
        output, _ = testing_utility.capture_print(account.delete, "test:")
        self.assertEqual(output, f'(lazy)> {lazy_constants.WARNING_COLOR}Invalid sequence provided. Make sure it '  # noqa
                                 f'contains at least 1 character and does not contain the following charaters:'
                                 f' " ,\' ,: ,; ,\ ,/ ,% , .{lazy_constants.RESET_COLOR}\n')

    def test_delete_account(self):
        testing_setup.create_test_account()
        account.delete("test")

        with open(lazy_constants.GENERAL_INFO_PATH) as f:
            active_user_line = f.readline()
        self.assertEqual(active_user_line, f"{lazy_constants.FILE_GENERAL_ACTIVE_USER}:\n")

        if Path(lazy_constants.USER_DIRS_PATH / "test").exists():
            self.fail("Account was not properly deleted upon calling delete")

    def test_get_username_password_no_set(self):
        name, pw = account._get_username_password("test")
        self.assertEqual(name, None)
        self.assertEqual(pw, None)

    def test_get_username_password_set(self):
        username = "test"
        password = "pw_test"
        account.new(username, password, password)
        name, pw = account._get_username_password("test")
        self.assertEqual(name, "test")
        self.assertEqual(pw, "pw_test")

    def test_equip_no_user_selected(self):
        testing_setup.create_test_account(activate=False)

        printed_text, _ = testing_utility.capture_print(account.equip, "stone axe")
        self.assertEqual(printed_text, f"(lazy)> {lazy_constants.WARNING_COLOR}No user selected. Select a user with "
                                       f"'account activate' or create a new one with 'account new'."
                                       f"{lazy_constants.RESET_COLOR}\n")
    #
    # def test_equip_
