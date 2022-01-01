from unittest import TestCase

import testing_setup
from src import utility, constants


class Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDownClass(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_is_valid_string_fail(self):
        self.assertFalse(utility.is_valid_string('"c'))
        self.assertFalse(utility.is_valid_string("'c"))
        self.assertFalse(utility.is_valid_string("adwdadw:"))
        self.assertFalse(utility.is_valid_string("dawd;"))
        self.assertFalse(utility.is_valid_string("daw\d"))
        self.assertFalse(utility.is_valid_string("dawd/"))
        self.assertFalse(utility.is_valid_string("d%awd"))
        self.assertFalse(utility.is_valid_string("da wd"))
        self.assertTrue(utility.is_valid_string("some_name"))

    def test_append_to_file(self):
        utility.append_to_file(constants.TEST_FILE, "one line\nanother line")
        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "one line\nanother line")
        testing_setup.clear_test_file()

    def test_set_values_in_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:value1\nname2:value2\n")

        utility.set_values_in_file(constants.TEST_FILE, ["name2", "name3"], ["new_value2", "value3"])

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:value1\nname2:new_value2\n")
        testing_setup.clear_test_file()

    def test_add_values_in_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        utility.add_values_in_file(constants.TEST_FILE, ["name2", "name3"], [2, 10], int)

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:1\nname2:4\nname3:10\n")
        testing_setup.clear_test_file()

    def test_get_values_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        values = utility.get_values_from_file(constants.TEST_FILE, ["name1", "name3"], int)

        self.assertEqual(values, [1])
        testing_setup.clear_test_file()

    def test_get_all_named_values_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        value_dict = utility.get_all_named_values_from_file(constants.TEST_FILE, int)

        self.assertEqual(value_dict, {"name1": 1, "name2": 2})
        testing_setup.clear_test_file()

    def test_remove_lines_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\nname3:1923")

        utility.remove_lines_from_file(constants.TEST_FILE, ["name1:1"])

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name2:2\nname3:1923")
        testing_setup.clear_test_file()

    def test_active_user_dir(self):
        path = utility.active_user_dir()
        self.assertEqual(str(constants.USER_DIRS_PATH / "test"), str(path))

    def test_active_user_area_dir(self):
        path = utility.active_user_area_dir()
        self.assertEqual(str(constants.USER_DIRS_PATH / "test" / constants.USER_AREA_DIR), str(path))
