from abc import ABC, abstractmethod

from src.items._items import Item


class ToolItem(Item, ABC):

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def TIME_REDUCTION(self) -> float:
        # a fraction that displays the time reduced for each roll
        pass

    # noinspection PyPep8Naming
    @property
    @abstractmethod
    def DURABILITY(self) -> int:
        # a fraction that displays the time reduced for each roll
        pass


class StoneAxeItem(ToolItem):
    TIME_REDUCTION: float = 0.0
    DURABILITY: int = 100
