from typing import Dict, List, Union, Set
from abc import ABC, abstractmethod
import random
from collections import defaultdict

# own imports
from src import constants
from src.skills import Skills
from src.items import Items


class Simulation(ABC):

    SIMULATE_EVERY: int = 60  # seconds

    def simulate(self, passed_time: int):
        # passed time is passed in seconds
        level_dict = defaultdict(int)
        item_dict = defaultdict(int)
        pass

    @abstractmethod
    def _simulate_roll(
        self,
        level_dict: defaultdict[str, int],
        item_dict: defaultdict[str, int]
    ):
        # return xp, items
        pass


class Area(Simulation):

    def __init__(self, name, locations, area_discovery_chance, description="",
                 unlocked_locations: Union[Set[str], None] = None):
        self.name = name
        self._locations = {location.name: location for location in locations}
        if constants.TESTING:
            for n in unlocked_locations:
                assert n in self._locations
        self._unlocked_locations = unlocked_locations if unlocked_locations is not None else set()
        self._locations_unlock_table = {location.name: location.discovery_chance for location in self._locations.values()
                                        if location.name not in self._unlocked_locations}
        self._unlock_chance = area_discovery_chance
        self.description = description

    def _simulate_roll(
        self,
        level_dict: defaultdict[str, int],
        item_dict: defaultdict[str, int]
    ):
        if random.random() < self._unlock_chance:
            unlocked_area = random.choices(list(self._locations_unlock_table.keys()),
                                           list(self._locations_unlock_table.values()), k=1)[0]
            level_dict[Skills.EXPLORING] += self._locations[unlocked_area].discover_xp
            del self._locations_unlock_table[unlocked_area]
            self._unlocked_locations.add(unlocked_area)


class Location:
    def __init__(self, name, chance, discover_xp, description=""):
        self.name = name
        self.discover_xp = discover_xp
        self.discovery_chance = chance
        self.description = description
        self._activities = []


class Activity(Simulation):
    def __init__(self, name, base_chance: float, action_table: Dict["Action", float], level_requirments: Dict[str, int],
                 item_requirements: List[str], description=""):
        self.name = name
        self._succes_chance = base_chance
        self._action_table = action_table
        self._level_requirements = level_requirments
        self._item_requirements = item_requirements
        self.description = description

    def _simulate_roll(
        self,
        level_dict: defaultdict[str, int],
        item_dict: defaultdict[str, int]
    ):
        if random.random() < self._succes_chance:
            action = random.choices(list(self._action_table.keys()),
                                    list(self._action_table.values()), k=1)[0]
            action.add_items_and_levels(level_dict, item_dict)


class Action:
    # something you do during an activity
    def __init__(
        self,
        name: str,
        item_rewards: Dict[str, int],
        xp_rewards: Dict[str, int],
        chance: float,
        description=""
    ):
        self.name = name
        self.roll_chance = chance
        self._item_rewards = item_rewards
        self._xp_rewards = xp_rewards
        self.description = description

    def add_items_and_levels(
        self,
        level_dict: defaultdict[str, int],
        item_dict: defaultdict[str, int]
    ):
        for skill in self._xp_rewards:
            level_dict[skill] += self._xp_rewards[skill]
        for item in self._item_rewards:
            item_dict[item] += self._item_rewards[item]


# green woods
_green_wood_location = Area("green woods", [], 0.25, "The starting are. The place one could call home.")


AREAS = {
    _green_wood_location.name: _green_wood_location
}
