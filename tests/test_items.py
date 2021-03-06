from unittest import TestCase

import testing_setup
import testing_utility
from lazy_src import items
from lazy_src import lazy_constants
from lazy_src.commands import account
from lazy_src import lazy_utility


class Test(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_folder()

    def test_inventory_load_no_user(self):
        testing_setup.create_test_account(activate=False)
        with self.assertRaises(SystemExit):
            items.get_inventory()

    def test_inventory_load_items(self):
        testing_setup.create_test_account()
        inv = items.get_inventory()
        self.assertDictEqual(inv.get_all_items(), {})

    def test_add_item_no_user(self):
        testing_setup.create_test_account()
        inventory = items.get_inventory()
        # get rid of active account
        account.delete("test")
        with self.assertRaises(SystemExit):
            inventory.add_items({})

    def test_add_items(self):
        testing_setup.create_test_account()
        inv = items.get_inventory()
        inv.add_items({items.Items.LOG.name: 5, items.Items.LEAF.name: 123})
        inv.add_items({items.Items.LOG.name: 10})
        current_user_dir = lazy_utility.active_user_dir()
        with open(current_user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            item_text = f.read()

        self.assertEqual(item_text, f"{items.Items.LOG.name}:15\n{items.Items.LEAF.name}:123\n")

    def test_add_invalid_item(self):
        testing_setup.create_test_account()
        inv = items.get_inventory()
        captured_text, _ = testing_utility.capture_print(inv.add_items, {"unknown item": 5, items.Items.LEAF.name: 123})
        self.assertEqual(captured_text, f"(lazy)> {lazy_constants.WARNING_COLOR}No item with name 'unknown item' "
                                        f"exists. This item will not be added to the inventroy."
                                        f"{lazy_constants.RESET_COLOR}\n")
        current_user_dir = lazy_utility.active_user_dir()
        with open(current_user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
            item_text = f.read()

        # make sure the other item was added
        self.assertEqual(item_text, f"{items.Items.LEAF.name}:123\n")

    def test_get_all_items(self):
        testing_setup.create_test_account()
        inv = items.get_inventory()
        inv.add_items({items.Items.LOG.name: 5, items.Items.LEAF.name: 1})
        inv.add_items({items.Items.LOG.name: 10})
        all_items = inv.get_all_items()

        self.assertDictEqual(all_items, {items.ITEM_MAPPING[items.Items.LOG.name]: 15,
                                         items.ITEM_MAPPING[items.Items.LEAF.name]: 1})

    def test_get_item_of_type(self):
        testing_setup.create_test_account()
        inv = items.get_inventory()
        inv.add_items({items.Items.LOG.name: 5, items.Items.LEAF.name: 1})
        inv.add_items({items.Items.LEATHER_BOOTS.name: 2})
        all_items = inv.get_all_of_type_items(items.WearableItem)

        self.assertDictEqual(all_items, {items.ITEM_MAPPING[items.Items.LEATHER_BOOTS.name]: 2})

    def test_get_equipment_no_user(self):
        testing_setup.create_test_account(activate=False)
        with self.assertRaises(SystemExit):
            items.get_equipment()

    def test_get_equipment(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        self.assertDictEqual(equipment.get_equiped_items(), {})

    def test_equip_item(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        equipment.equip_items({items.WearableItem.BACK: items.Items.BLACK_CAPE})
        self.assertDictEqual(equipment.get_equiped_items(), {items.WearableItem.BACK: items.Items.BLACK_CAPE})

    def test_double_equip_item(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        equipment.equip_items({items.WearableItem.BACK: items.Items.BLACK_CAPE})
        equipment.equip_items({items.WearableItem.BACK: items.Items.PINK_CAPE})
        self.assertDictEqual(equipment.get_equiped_items(), {items.WearableItem.BACK: items.Items.PINK_CAPE})

    def test_equip_invalid_slot(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        captured_text, _ = testing_utility.capture_print(equipment.equip_items, {"Me head": items.Items.BLACK_CAPE})
        self.assertEqual(captured_text, f"(lazy)> {lazy_constants.WARNING_COLOR}No equipment slot with name 'Me head'"
                                        f"{lazy_constants.RESET_COLOR}\n")

    def test_get_equipment_at_slot(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        equipment.equip_items({items.WearableItem.BACK: items.Items.BLACK_CAPE})
        item = equipment.get_equipment_at_slot(items.WearableItem.BACK)
        self.assertEqual(item, items.Items.BLACK_CAPE)

    def test_get_equipment_at_slot_(self):
        testing_setup.create_test_account()
        equipment = items.get_equipment()
        equipment.equip_items({items.WearableItem.BACK: items.Items.BLACK_CAPE})
        with self.assertRaises(SystemExit):
            equipment.get_equipment_at_slot("unexisting slot")