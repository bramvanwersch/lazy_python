from lazy_src.items._items import *


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
    OLD_BREAD = FoodItem("old_bread", "Stale without fail.", 1)
    SMALL_DAGGER = WeaponItem("small dagger", "Small stabber.", 2)
    LEATHER_BOOTS = EquipmentItem("leather boots", "Durable protectors of feat.", 1)
    BLACK_CAPE = EquipmentItem("black cape", "Look mom, I AM BATMAN", 1)
    STONE_AXE = ToolItem("stone axe", "This presumably allows for cutting wood", 0.05, 100)
    TROUT = FoodItem("trout", "A grayt(ish) fish.", 1)
    SALMON = FoodItem("salmon", "I love to eat this with dill", 2)
    SHRIMP = FoodItem("shrimp", "I loveee shrimp.", 0)
    OLD_BOOT = GeneralItem("old boot", "Who leaves a perfectly fine boot like that... Oh nevermind. Yuck.")

    @classmethod
    def all_items(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname not in ["all_items"]]


ITEM_MAPPING = {item.name: item for item in Items.all_items()}
