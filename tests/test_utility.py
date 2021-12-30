from unittest import TestCase
import os
from pathlib import Path
import subprocess


from src import utility, constants


class Test(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # create account named test
        process = subprocess.Popen("lazy account new test test test")
        process.wait()
        process = subprocess.Popen("lazy account load test test")
        process.wait()
        try:
            os.mkdir(constants.TEST_FOLDER)
        except IOError:
            pass
        # reset / create the test_file
        cls._clear_test_file()

    @classmethod
    def tearDownClass(cls) -> None:
        # clean up leftovers
        os.remove(constants.TEST_FILE)
        os.rmdir(constants.TEST_FOLDER)
        process = subprocess.Popen("lazy account delete test")
        process.wait()

    @classmethod
    def _clear_test_file(cls):
        open(constants.TEST_FILE, "w").close()

    def test_is_valid_string_fail(self):
        self.assertFalse(utility.is_valid_string('"c'))
        self.assertFalse(utility.is_valid_string("'c"))
        self.assertFalse(utility.is_valid_string("adwdadw:"))
        self.assertFalse(utility.is_valid_string("dawd;"))
        self.assertFalse(utility.is_valid_string("daw\d"))
        self.assertFalse(utility.is_valid_string("dawd/"))
        self.assertFalse(utility.is_valid_string("d%awd"))
        self.assertFalse(utility.is_valid_string("da wd"))

    def test_append_to_file(self):
        utility.append_to_file(constants.TEST_FILE, "one line\nanother line")
        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "one line\nanother line")
        self._clear_test_file()

    def test_set_values_in_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:value1\nname2:value2\n")

        utility.set_values_in_file(constants.TEST_FILE, ["name2", "name3"], ["new_value2", "value3"])

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:value1\nname2:new_value2\n")
        self._clear_test_file()

    def test_add_values_in_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        utility.add_values_in_file(constants.TEST_FILE, ["name2", "name3"], [2, 10], int)

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:1\nname2:4\nname3:10\n")
        self._clear_test_file()

    def test_get_values_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        values = utility.get_values_from_file(constants.TEST_FILE, ["name1", "name3"], int)

        self.assertEqual(values, [1])
        self._clear_test_file()

    def test_get_all_named_values_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        value_dict = utility.get_all_named_values_from_file(constants.TEST_FILE, int)

        self.assertEqual(value_dict, {"name1": 1, "name2": 2})
        self._clear_test_file()

    def test_remove_lines_from_file(self):
        # setup the file
        with open(constants.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\nname3:1923")

        utility.remove_lines_from_file(constants.TEST_FILE, ["name1:1"])

        with open(constants.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name2:2\nname3:1923")
        self._clear_test_file()

    def test_active_user_dir(self):
        path = utility.active_user_dir()
        self.assertEqual(str(constants.USER_DIRS_PATH / "test"), str(path))

    def test_active_user_area_dir(self):
        path = utility.active_user_area_dir()
        self.assertEqual(str(constants.USER_DIRS_PATH / "test" / constants.USER_AREA_DIR), str(path))
