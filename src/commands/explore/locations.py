from typing import Dict, List, Union, Set, DefaultDict
from abc import ABC, abstractmethod
import random
from collections import defaultdict

# own imports
from src import constants
from src import skills
from src import items


class Simulation(ABC):

    SIMULATE_EVERY: int = 60  # seconds

    def simulate(self, passed_time: int):
        # passed time is passed in seconds
        xp_dict = defaultdict(int)
        item_dict = defaultdict(int)
        for _ in range(passed_time % self.SIMULATE_EVERY):
            self._simulate_roll(xp_dict, item_dict)
            skills.add_xp(xp_dict)
            items.add_items(item_dict)

    @abstractmethod
    def _simulate_roll(
        self,
        xp_dict: DefaultDict[str, int],
        item_dict: DefaultDict[str, int]
    ):
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
        self._locations_unlock_table = \
            {location.name: location.discovery_chance for location in self._locations.values() 
             if location.name not in self._unlocked_locations}
        self._unlock_chance = area_discovery_chance
        self.description = description

    def _simulate_roll(
        self,
        xp_dict: DefaultDict[str, int],
        item_dict: DefaultDict[str, int]
    ):
        additional_skill_chance = skills.get_level(skills.Skills.EXPLORING.name)
        if random.random() < self._unlock_chance + additional_skill_chance:
            unlocked_area = random.choices(list(self._locations_unlock_table.keys()),
                                           list(self._locations_unlock_table.values()), k=1)[0]
            xp_dict[skills.Skills.EXPLORING] += self._locations[unlocked_area].discover_xp
            del self._locations_unlock_table[unlocked_area]
            self._unlocked_locations.add(unlocked_area)


class Location:
    def __init__(self, name, chance, discover_xp, activities, description=""):
        self.name = name
        self.discover_xp = discover_xp
        self.discovery_chance = chance
        self.description = description
        self._activities = activities


class Activity(Simulation):
    def __init__(self, name, main_skill, base_chance: float, loot_list: List["Loot"], level_requirments: Dict[str, int]
                 , description=""):
        self.name = name
        self._main_skill = main_skill
        self._succes_chance = base_chance
        self._loot_table = {loot: loot.roll_weight for loot in loot_list}
        self._level_requirements = level_requirments
        self.description = description

    def _simulate_roll(
        self,
        xp_dict: DefaultDict[str, int],
        item_dict: DefaultDict[str, int]
    ):
        additional_skill_chance = skills.get_level(self._main_skill.name)
        if random.random() < self._succes_chance + additional_skill_chance:
            loot = random.choices(list(self._loot_table.keys()), list(self._loot_table.values()), k=1)[0]
            loot.add_xp_and_items(xp_dict, item_dict)
            if loot.is_depleted():
                del self._loot_table[loot]


class Loot:
    def __init__(
        self,
        item_rewards: Dict[str, int],
        xp_rewards: Dict[str, int],
        chance: float,
        max_supply: int = None
    ):
        self.roll_weight = chance
        self._item_rewards = item_rewards
        self._xp_rewards = xp_rewards
        self._max_supply = max_supply

    def is_depleted(self):
        if self.is_depletable() is False:
            return False
        return self._max_supply <= 0

    def is_depletable(self):
        return self._max_supply is not None

    def add_xp_and_items(
        self,
        xp_dict: DefaultDict[str, int],
        item_dict: DefaultDict[str, int]
    ):
        for skill in self._xp_rewards:
            xp_dict[skill] += self._xp_rewards[skill]
        for item in self._item_rewards:
            item_dict[item] += self._item_rewards[item]

        if self._max_supply is not None:
            self._max_supply -= 1
