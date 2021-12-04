from abc import ABC

from src import utility
from src import constants


class Item(ABC):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return other.name == self.name


# general utility functions related to player

def add_items(item_dict):
    user_dir = utility.active_user_dir()
    utility.add_values_in_file(user_dir / constants.USER_INVENTORY_FILE_NAME,
                               [item.name for item in item_dict.keys()], item_dict.values(), int)


def get_all_items():
    user_dir = utility.active_user_dir()
    return utility.get_all_named_values_from_file(user_dir / constants.USER_INVENTORY_FILE_NAME, int)
