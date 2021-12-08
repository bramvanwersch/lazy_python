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


class GeneralItem(Item):
    pass


class FoodItem(Item, ABC):

    def __init__(self, name, health_restored):
        super().__init__(name)
        self._health_restored = health_restored

    @property
    def health_restored(self):
        return self._health_restored


class EquipmentItem(Item, ABC):

    def __init__(self, name, armour):
        super().__init__(name)
        self._armour = armour

    @property
    def armour(self):
        return self._armour


class ToolItem(Item, ABC):

    def __init__(self, name, time_reduction, durability):
        super().__init__(name)
        self._time_reduction = time_reduction
        self._durability = durability

    @property
    def time_reduction(self):
        return self._time_reduction

    @property
    def durability(self):
        return self._durability


class WeaponItem(Item, ABC):

    def __init__(self, name, damage):
        super().__init__(name)
        self._damage = damage

    @property
    def damage(self):
        return self._damage


# general utility functions related to player

def add_items(item_dict):
    user_dir = utility.active_user_dir()
    utility.add_values_in_file(user_dir / constants.USER_INVENTORY_FILE_NAME,
                               [item.name for item in item_dict.keys()], item_dict.values(), int)


def get_all_items():
    user_dir = utility.active_user_dir()
    return utility.get_all_named_values_from_file(user_dir / constants.USER_INVENTORY_FILE_NAME, int)
