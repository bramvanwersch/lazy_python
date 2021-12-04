from src.commands.explore.locations import *
from src.items import Items
from src.skills import Skills


# green woods

# loot

_old_bread_loot = Loot({Items.OLD_BREAD: 1}, {}, 1)
_forgotten_stuff = Loot({Items.SMALL_DAGGER: 1, Items.BLACK_CAPE: 1, Items.LEATHER_BOOTS: 1},
                        {Skills.GATHERING: 50}, 0.1, 1)
_1_coin_loot = Loot({Items.COIN: 1}, {Skills.GATHERING: 1}, 2)
_10_coin_loot = Loot({Items.COIN: 10}, {Skills.GATHERING: 4}, 0.5)
_15_coin_loot = Loot({Items.COIN: 15}, {Skills.GATHERING: 8}, 0.5)
_20_coin_loot = Loot({Items.COIN: 20}, {Skills.GATHERING: 10}, 0.05)
_cobweb_loot = Loot({Items.COBWEB: 1}, {}, 4)
_brown_mushroom_loot = Loot({Items.B_MUSHROOM: 1}, {Skills.GATHERING: 2}, 1)
_red_mushroom_loot = Loot({Items.R_MUSHROOM: 1}, {Skills.GATHERING: 4}, 0.2)
_yellow_mushroom_loot = Loot({Items.Y_MUSHROOM: 1}, {Skills.GATHERING: 20}, 0.001)

_tree_loots = [_1_coin_loot, _10_coin_loot, _15_coin_loot, _20_coin_loot, _cobweb_loot, _brown_mushroom_loot,
               _red_mushroom_loot, _yellow_mushroom_loot]

_home_loots = [_1_coin_loot, _old_bread_loot, _forgotten_stuff]

# activities
_old_tree_gather = Activity("gathering", 0.25, _tree_loots, {}, [],
                            "There might be some things left around by other people")
_old_tree_chopping = Activity("woodcutting", 0.25)
_old_tree_activities = [_old_tree_gather]

_home_gather = Activity("gathering", 0.05, _home_loots, {}, [],
                        "There might be some supplies left, on the other hand there is a reason im leaving.")


# locations
_old_tree_location = Location("Old tree", 0.4, 5, _old_tree_activities,
                              "An old looking tree. Does not look like there is a lot of interesting things to "
                              "find here.")
_player_home = Location("Home", 0.0, 0, [_home_gather],
                        "A place with good and bad memories")


_green_wood_area = Area("green woods", [_old_tree_location, _player_home], 0.25,
                        "The starting are. The place I grew up in and call home.",
                        {_player_home.name})


AREAS = {
    _green_wood_area.name: _green_wood_area
}
