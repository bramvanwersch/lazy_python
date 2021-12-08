from src.areas.locations import *
from src.items import Items
from src.skills import Skills


# green woods

# loot

# home
_old_bread_loot = Loot({Items.OLD_BREAD: 1}, {}, 1)
_forgotten_stuff = Loot({Items.SMALL_DAGGER: 1, Items.BLACK_CAPE: 1, Items.LEATHER_BOOTS: 1},
                        {Skills.GATHERING: 50}, 0.1, 1)
# tree gather
_1_coin_loot = Loot({Items.COIN: 1}, {Skills.GATHERING: 1}, 2)
_10_coin_loot = Loot({Items.COIN: 10}, {Skills.GATHERING: 4}, 0.5)
_15_coin_loot = Loot({Items.COIN: 15}, {Skills.GATHERING: 8}, 0.5)
_20_coin_loot = Loot({Items.COIN: 20}, {Skills.GATHERING: 10}, 0.05)
_cobweb_loot = Loot({Items.COBWEB: 1}, {}, 4)
_brown_mushroom_loot = Loot({Items.B_MUSHROOM: 1}, {Skills.GATHERING: 2}, 1)
_red_mushroom_loot = Loot({Items.R_MUSHROOM: 1}, {Skills.GATHERING: 4}, 0.2)
_yellow_mushroom_loot = Loot({Items.Y_MUSHROOM: 1}, {Skills.GATHERING: 20}, 0.001)

# tree woodcut
_log_loot = Loot({Items.LOG: 1}, {Skills.WOODCUTTING: 5}, 1)
_branch_loot = Loot({Items.BRANCH: 1}, {Skills.WOODCUTTING: 2}, 0.5)
_leaf_loot = Loot({Items.LEAF: 15}, {Skills.WOODCUTTING: 1}, 0.2)
_birdnest_loot = Loot({Items.BIRDSNEST: 1, Items.EGG: 1}, {}, 0.05)

_tree_gather_loots = [_1_coin_loot, _10_coin_loot, _15_coin_loot, _20_coin_loot, _cobweb_loot, _brown_mushroom_loot,
                      _red_mushroom_loot, _yellow_mushroom_loot]
_tree_woodcut_loots = [_log_loot, _branch_loot, _leaf_loot, _birdnest_loot]

_home_loots = [_1_coin_loot, _old_bread_loot, _forgotten_stuff]

# activities
_old_tree_gather = Activity("gathering", Skills.GATHERING, 0.25, _tree_gather_loots, {},
                            "There might be some things left around by other people.")
_old_tree_chopping = Activity("woodcutting", Skills.WOODCUTTING, 0.25, _tree_woodcut_loots, {},
                              "The old tree cna be chopped it never seems to get smaller though.")
_old_tree_activities = [_old_tree_gather, _old_tree_chopping]

_home_gather = Activity("gathering", Skills.GATHERING, 0.05, _home_loots, {},
                        "There might be some supplies left, on the other hand there is a reason im leaving.")


# locations
_old_tree_location = Location("Old tree", 0.4, 5, _old_tree_activities,
                              "An old looking tree. Does not look like there is a lot of interesting things to "
                              "find here.")

_player_home = Location("Home", 0.0, 0, [_home_gather],
                        "A place with good and bad memories")

# area definition
green_woods = _green_wood_area = Area("green woods", [_old_tree_location, _player_home], 0, 0.25, 10,
                                      "The starting are. The place I grew up in and call home.")
