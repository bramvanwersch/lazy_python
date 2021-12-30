from unittest import TestCase
import os
from pathlib import Path


from lazy import utility


class Test(TestCase):

    TEST_FOLDER = Path(__file__).resolve().parent / "test_dump"
    TEST_FILE = TEST_FOLDER / "test_file.txt"

    @classmethod
    def setUpClass(cls) -> None:
        try:
            os.mkdir(cls.TEST_FOLDER)
        except IOError:
            pass
        # reset / create the test_file
        cls._clear_test_file()

    @classmethod
    def tearDownClass(cls) -> None:
        # clean up leftovers
        os.remove(cls.TEST_FILE)
        os.rmdir(cls.TEST_FOLDER)

    @classmethod
    def _clear_test_file(cls):
        open(cls.TEST_FILE, "w").close()

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
        utility.append_to_file(self.TEST_FILE, "one line\nanother line")
        with open(self.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "one line\nanother line")
        self._clear_test_file()

    def test_set_values_in_file(self):
        # setup the file
        with open(self.TEST_FILE, "w") as f:
            f.write("name1:value1\nname2:value2\n")

        utility.set_values_in_file(self.TEST_FILE, ["name2", "name3"], ["new_value2", "value3"])

        with open(self.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:value1\nname2:new_value2\n")
        self._clear_test_file()

    def test_add_values_in_file(self):
        # setup the file
        with open(self.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        utility.add_values_in_file(self.TEST_FILE, ["name2", "name3"], [2, 10], int)

        with open(self.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name1:1\nname2:4\nname3:10\n")
        self._clear_test_file()

    def test_get_values_from_file(self):
        # setup the file
        with open(self.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        values = utility.get_values_from_file(self.TEST_FILE, ["name1", "name3"], int)

        self.assertEqual(values, [1])
        self._clear_test_file()

    def test_get_all_named_values_from_file(self):
        # setup the file
        with open(self.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\n")

        value_dict = utility.get_all_named_values_from_file(self.TEST_FILE, int)

        self.assertEqual(value_dict, {"name1": 1, "name2": 2})
        self._clear_test_file()

    def test_remove_lines_from_file(self):
        # setup the file
        with open(self.TEST_FILE, "w") as f:
            f.write("name1:1\nname2:2\nname3:1923")

        utility.remove_lines_from_file(self.TEST_FILE, ["name1:1"])

        with open(self.TEST_FILE) as f:
            text = f.read()
        self.assertEqual(text, "name2:2\nname3:1923")
        self._clear_test_file()
