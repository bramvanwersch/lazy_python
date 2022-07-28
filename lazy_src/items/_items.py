from abc import ABC
from typing import Dict

from lazy_src import lazy_utility
from lazy_src import lazy_constants


class Item(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def examine_text(self):
        return f"{self.name}: {self.description}"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return other.name == self.name


class GeneralItem(Item):
    pass


class FoodItem(Item, ABC):

    def __init__(self, name, description, health_restored):
        super().__init__(name, description)
        self._health_restored = health_restored

    @property
    def health_restored(self):
        return self._health_restored


class EquipmentItem(Item, ABC):

    def __init__(self, name, description, armour):
        super().__init__(name, description)
        self._armour = armour

    @property
    def armour(self):
        return self._armour


class ToolItem(Item, ABC):

    def __init__(self, name, description, time_reduction, durability):
        super().__init__(name, description)
        self._time_reduction = time_reduction
        self._durability = durability

    @property
    def time_reduction(self):
        return self._time_reduction

    @property
    def durability(self):
        return self._durability


class WeaponItem(Item, ABC):

    def __init__(self, name, description, damage):
        super().__init__(name, description)
        self._damage = damage

    @property
    def damage(self):
        return self._damage


# general utility functions related to player

def add_items(item_dict: Dict[str, int]):
    user_dir = lazy_utility.active_user_dir()
    lazy_utility.add_values_in_file(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME,
                                    list(item for item in item_dict.keys()), list(item_dict.values()), int)


def get_all_items():
    user_dir = lazy_utility.active_user_dir()
    return lazy_utility.get_all_named_values_from_file(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME, int)
