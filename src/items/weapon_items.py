from abc import ABC, abstractmethod

from src.items._items import Item


class WeaponItem(Item, ABC):

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def DAMAGE(self) -> int:
        pass


class SmallDaggerItem(WeaponItem):
    DAMAGE: int = 2
