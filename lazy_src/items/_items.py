from abc import ABC
from typing import Dict, List

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


class FoodItem(Item):

    def __init__(self, name, description, health_restored):
        super().__init__(name, description)
        self._health_restored = health_restored

    @property
    def health_restored(self):
        return self._health_restored


class WearableItem(Item, ABC):
    HEAD: str = "head"
    BACK: str = "back"
    CHEST: str = "chest"
    LEFT_HAND: str = "left"
    RIGHT_HAND: str = "rigth"
    LEGS: str = "pants"
    RING: str = "ring"
    AMULET: str = "amulet"
    FEET: str = "boots"

    def __init__(
        self,
        name: str,
        description: str,
        slot: str
    ):
        super().__init__(name, description)
        self.slot = None
        self._set_slot(slot)

    @classmethod
    def all_equipment_slots(cls) -> List[str]:
        return [cls.HEAD, cls.BACK, cls.CHEST, cls.LEFT_HAND, cls.RIGHT_HAND, cls.LEGS,
                cls.RING, cls.AMULET, cls.FEET]

    def _set_slot(self, value: str):
        if value not in self.all_equipment_slots():
            raise ValueError(f"Invalid slot provided for {self.name}")
        self.slot = value


class EquipmentItem(WearableItem):

    def __init__(self, name, description, armour, slot):
        super().__init__(name, description, slot)
        self._armour = armour

    @property
    def armour(self):
        return self._armour


class ToolItem(WearableItem):

    def __init__(self, name, description, time_reduction, durability, slot):
        super().__init__(name, description, slot)
        self._time_reduction = time_reduction
        self._durability = durability

    @property
    def time_reduction(self):
        return self._time_reduction

    @property
    def durability(self):
        return self._durability


class WeaponItem(WearableItem):

    def __init__(self, name, description, damage, slot):
        super().__init__(name, description, slot)
        self._damage = damage

    @property
    def damage(self):
        return self._damage


class Items:

    LOG = GeneralItem("log", "This can be used for all sorts of things")
    BIRDSNEST = GeneralItem("birdsnest", "")
    EGG = FoodItem("egg", "Nicely egg shaped. I can cook with this.", 1)
    BRANCH = GeneralItem("branch", "Like a long stick.")
    LEAF = GeneralItem("leaf", "Leaf me alone.")
    COBWEB = GeneralItem("cobweb", "Lots of silky smooth string.")
    COIN = GeneralItem("coin", "The facilitator of capitalism")
    SILVER_COIN = GeneralItem("silver coin", "Like a coin but silver (so more expensive).")
    B_MUSHROOM = FoodItem("brown mushroom", "I think this one is edible", 1)
    R_MUSHROOM = FoodItem("red mushroom", "I realy hope this one is edible. I am afraid my friend hoped the same. "
                                          "RIP james :(.", -1)
    Y_MUSHROOM = FoodItem("yellow mushroom", "A quite rare find, but very delicious.", 5)
    OLD_BREAD = FoodItem("old bread", "Stale without fail.", 1)
    SMALL_DAGGER = WeaponItem("small dagger", "Small stabber.", 2, WearableItem.RIGHT_HAND)
    LEATHER_BOOTS = EquipmentItem("leather boots", "Durable protectors of feat.", 1, WearableItem.FEET)
    BLACK_CAPE = EquipmentItem("black cape", "Look mom, I AM BATMAN", 1, WearableItem.BACK)
    PINK_CAPE = EquipmentItem("pink cape", "Ohh my god I look so fab, UwU!", 1, WearableItem.BACK)
    STONE_AXE = ToolItem("stone axe", "This presumably allows for cutting wood", 0.05, 100, WearableItem.RIGHT_HAND)
    TROUT = FoodItem("trout", "A grayt(ish) fish.", 1)
    SALMON = FoodItem("salmon", "I love to eat this with dill", 2)
    SHRIMP = FoodItem("shrimp", "I loveee shrimp.", 0)
    OLD_BOOT = GeneralItem("old boot", "Who leaves a perfectly fine boot like that... Oh nevermind. Yuck.")
    PEBBLE = GeneralItem("pebble", "A simple rock.")
    IRON_NUGGET = GeneralItem("iron nugget", "A small piece of iron.")
    MYSTERY_STONE = GeneralItem("mystery stone", "What is in it?")
    GOLD_NUGGET = GeneralItem("gold nugget", "A small piece of gold.")
    ROCK = GeneralItem("rock", "It's not just a rock its a boulder!")
    COAL_CHUNK = GeneralItem("coal chunk", "A piece of coal, luckily it is not christmas.")
    IRON_ORE = GeneralItem("iron ore", "A large piece of iron.")

    @classmethod
    def all_items(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname not in ["all_items"]]


ITEM_MAPPING = {item.name: item for item in Items.all_items()}
