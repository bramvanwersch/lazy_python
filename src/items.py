from src import constants
from src import utility


class Items:

    LOG = "log"
    OAK_LOG = "oak log"
    BRANCH = "branch"
    LEAF = "leaf"
    COBWEB = "cobweb"
    COIN = "coin"
    SILVER_COIN = "silver coin"
    B_MUSHROOM = "brown mushroom"
    R_MUSHROOM = "red mushroom"
    Y_MUSHROOM = "yellow mushroom"
    OLD_BREAD = "old_bread"
    SMALL_DAGGER = "small dagger"
    LEATHER_BOOTS = "leather boos"
    BLACK_CAPE = "black cape"


def add_items(item_dict):
    user_dir = utility.active_user_dir()
    utility.add_values_in_file(user_dir / constants.USER_INVENTORY_FILE_NAME, item_dict.keys(), item_dict.values(), int)


def get_all_items():
    user_dir = utility.active_user_dir()
    return utility.get_all_named_values_from_file(user_dir / constants.USER_INVENTORY_FILE_NAME, int)




# class Item:
#     def __init__(self, name, quantity):
#         self.name = name
#         self.quantity = quantity
#
#     def __hash__(self):
#         return hash((self.name, self.quantity))
#
#     def __eq__(self, other):
#         if isinstance(other, Item):
#             return other.name == other.quantity
#         return False
