from unittest import TestCase

import testing_setup
from src import items
from src import constants
from src import utility


class Test(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_add_items(self):
        items.add_items({"item_name": 5, "other_item": 123})
        items.add_items({"item_name": 10})
        current_user_dir = utility.active_user_dir()
        with open(current_user_dir / constants.USER_INVENTORY_FILE_NAME) as f:
            item_text = f.read()

        self.assertEqual(item_text, "item_name:15\nother_item:123\n")

    def test_get_all_items(self):
        items.add_items({"item_name": 15, "other_item": 1})
        items.add_items({"item_name": 10})
        all_items = items.get_all_items()

        self.assertEqual(all_items, {"item_name": 25, "other_item": 1})
