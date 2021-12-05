from src.items.food_items import *
from src.items.equipment_items import *
from src.items.weapon_items import *
from src.items.general_items import *
from src.items.tool_items import *
from src.items._items import *


class Items:

    LOG = GeneralItem("log")
    BIRDSNEST = GeneralItem("birdsnest")
    EGG = EggItem("egg")
    BRANCH = GeneralItem("branch")
    LEAF = GeneralItem("leaf")
    COBWEB = GeneralItem("cobweb")
    COIN = GeneralItem("coin")
    SILVER_COIN = GeneralItem("silver coin")
    B_MUSHROOM = BrownMushroomItem("brown mushroom")
    R_MUSHROOM = RedMushroomItem("red mushroom")
    Y_MUSHROOM = YellowMushroomItem("yellow mushroom")
    OLD_BREAD = OldBreadItem("old_bread")
    SMALL_DAGGER = SmallDaggerItem("small dagger")
    LEATHER_BOOTS = LeatherBootsItem("leather boots")
    BLACK_CAPE = BlackCapeItem("black cape")
    STONE_AXE = StoneAxeItem("stone axe")

    @classmethod
    def all_items(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname not in ["all_items"]]


ITEM_MAPPING = {item.name: item for item in Items.all_items()}
