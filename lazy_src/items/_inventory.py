from typing import Dict, Type

from lazy_src.items._items import ITEM_MAPPING, Item
from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings


def get_inventory() -> "_Inventory":
    # will exit if no active user
    return _Inventory()


class _Inventory:

    items: Dict[Item, int]

    def __init__(self):
        self._items = {}
        self._load()

    def _load(self):
        # will exit if no user is seleceted
        user_dir = lazy_utility.active_user_dir()
        items = lazy_utility.get_all_named_values_from_file(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME, int)
        self._items = {ITEM_MAPPING[name]: amnt for name, amnt in items.items()}

    def get_all_items(self) -> Dict[Item, int]:
        return self._items

    def add_items(
        self,
        item_dict: Dict[str, int]
    ):
        # will exit on no selected user
        user_dir = lazy_utility.active_user_dir()
        # save into new dictionary to not modify the supplied one
        accepted_items = {}
        for name, amnt in item_dict.items():
            if name not in ITEM_MAPPING:
                lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_ITEM_NAME,
                                   extra_info=" This item will not be added to the inventroy.", name=name)
            else:
                accepted_items[name] = amnt
        lazy_utility.add_values_in_file(
            user_dir / lazy_constants.USER_INVENTORY_FILE_NAME,
            list(item for item in accepted_items.keys()), list(accepted_items.values()), int)
        self._load()

    def get_all_of_type_items(
        self,
        type_: Type[Item]
    ) -> Dict[Item, int]:
        item_dict = {}
        for item, amnt in self._items.items():
            if isinstance(item, type_):
                item_dict[item] = amnt
        return item_dict
