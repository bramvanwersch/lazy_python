from lazy_src.items._items import *


class Items:

    LOG = GeneralItem("log")
    BIRDSNEST = GeneralItem("birdsnest")
    EGG = FoodItem("egg", 1)
    BRANCH = GeneralItem("branch")
    LEAF = GeneralItem("leaf")
    COBWEB = GeneralItem("cobweb")
    COIN = GeneralItem("coin")
    SILVER_COIN = GeneralItem("silver coin")
    B_MUSHROOM = FoodItem("brown mushroom", 1)
    R_MUSHROOM = FoodItem("red mushroom", -1)
    Y_MUSHROOM = FoodItem("yellow mushroom", 5)
    OLD_BREAD = FoodItem("old_bread", 1)
    SMALL_DAGGER = WeaponItem("small dagger", 2)
    LEATHER_BOOTS = EquipmentItem("leather boots", 1)
    BLACK_CAPE = EquipmentItem("black cape", 1)
    STONE_AXE = ToolItem("stone axe", 0.05, 100)
    TROUT = FoodItem("trout", 1)
    SALMON = FoodItem("salmon", 2)
    SHRIMP = FoodItem("shrimp", 0)
    OLD_BOOT = GeneralItem("old boot")

    @classmethod
    def all_items(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname not in ["all_items"]]


ITEM_MAPPING = {item.name: item for item in Items.all_items()}
