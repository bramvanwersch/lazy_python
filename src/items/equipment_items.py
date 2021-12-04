from abc import ABC, abstractmethod

from src.items._items import Item


class EquipmentItem(Item, ABC):

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def ARMOUR(self) -> int:
        pass


class BlackCapeItem(EquipmentItem):
    ARMOUR: int = 1


class LeatherBootsItem(EquipmentItem):
    ARMOUR: int = 1