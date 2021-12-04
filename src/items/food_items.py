from abc import ABC, abstractmethod

from src.items._items import Item


class FoodItem(Item, ABC):

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def HEALTH_RESTORED(self) -> int:
        pass


class EggItem(FoodItem):
    HEALTH_RESTORED: int = 1


class BrownMushroomItem(FoodItem):
    HEALTH_RESTORED: int = 1


class RedMushroomItem(FoodItem):
    HEALTH_RESTORED: int = -1


class YellowMushroomItem(FoodItem):
    HEALTH_RESTORED: int = 5


class OldBreadItem(FoodItem):
    HEALTH_RESTORED: int = 1
