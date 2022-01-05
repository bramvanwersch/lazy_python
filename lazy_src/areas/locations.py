from typing import Dict, List, DefaultDict, Set
from abc import ABC, abstractmethod
import random
from collections import defaultdict

# own imports
from lazy_src import lazy_constants
from lazy_src import skills
from lazy_src import items
from lazy_src import lazy_utility


# general functions
def get_unlocked_location_names(current_area: str = None) -> Set[str]:
    if current_area is None:
        current_area = lazy_utility.get_values_from_file(lazy_utility.active_user_dir() /
                                                         lazy_constants.USER_GENERAL_FILE_NAME, ["current_area"])[0]
    unlocked_locations = lazy_utility.get_values_from_file(lazy_utility.active_user_area_dir() / current_area,
                                                           ["unlocked_locations"])[0]
    unlocked_locations = set(unlocked_locations.split(","))
    return unlocked_locations


# objects
class Simulation(ABC):

    SIMULATE_EVERY: int = 60  # seconds

    def simulate(self, passed_time: int):
        # passed time is passed in seconds
        xp_dict = skills.get_xps()
        item_dict = defaultdict(int)
        for _ in range(int(passed_time / self.SIMULATE_EVERY)):
            self._simulate_roll(xp_dict, item_dict)
        return xp_dict, item_dict

    @abstractmethod
    def _simulate_roll(
        self,
        xp_dict: Dict[str, int],
        item_dict: DefaultDict[str, int]
    ):
        pass


class Area:
    SIMULATE_EVERY: int = 60  # seconds

    def __init__(self, name, locations, level, location_discovery_chance, repeated_discover_xp, description=""):
        self.name = name
        self._no_find_xp = repeated_discover_xp
        self.required_level = level
        self._locations = {location.name: location for location in locations}
        self._unlock_chance = location_discovery_chance
        self.description = description

    def examine(self):
        description = f"{self.name.upper()}:\n{self.description}\nLocations:\n"
        unlocked_locations = get_unlocked_location_names()
        for location_name in self._locations:
            if location_name in unlocked_locations:
                description += f"- {location_name}: {self._locations[location_name].description}\n"
            else:
                description += f"- ???: ???\n"
        lazy_utility.message(description[:-1])  # remove last newline

    def perform_activity_rolls(self, location, activity, passed_time):
        if activity == "exploring":
            unlocked_locations = get_unlocked_location_names()
            return self._discover_areas(passed_time, unlocked_locations)
        else:
            return self._locations[location].activities[activity].simulate(passed_time)

    @property
    def locations(self) -> Dict[str, "Location"]:
        # make it sort of read only
        return self._locations

    def _discover_areas(
        self,
        passed_time: int,
        unlocked_locations: Set[str]
    ):
        xp_dict = skills.get_xps()
        item_dict = defaultdict(int)
        locations_unlock_table = {location: location.discovery_chance for location_name, location
                                  in self._locations.items() if location_name not in unlocked_locations}
        for _ in range(int(passed_time / self.SIMULATE_EVERY)):
            all_xp = xp_dict[skills.Skills.EXPLORING.name]
            additional_skill_chance = skills.Skills.EXPLORING.get_additional_roll_chance(all_xp)
            if random.random() < self._unlock_chance + additional_skill_chance:
                if len(locations_unlock_table) != 0:
                    unlocked_area = random.choices(list(locations_unlock_table.keys()),
                                                   list(locations_unlock_table.values()), k=1)[0]
                    xp_dict[skills.Skills.EXPLORING.name] += unlocked_area.discover_xp
                    item_dict[unlocked_area.name] = 1
                    del locations_unlock_table[unlocked_area]
                    unlocked_locations.add(unlocked_area.name)
                else:
                    xp_dict[skills.Skills.EXPLORING.name] += self._no_find_xp
        current_area = lazy_utility.get_values_from_file(lazy_utility.active_user_dir() /
                                                         lazy_constants.USER_GENERAL_FILE_NAME, ["current_area"])[0]
        lazy_utility.set_values_in_file(lazy_utility.active_user_area_dir() / current_area, ["unlocked_locations"],
                                        [','.join(unlocked_locations)])
        return xp_dict, item_dict


class Location:
    def __init__(self, name, chance, discover_xp, activities, description=""):
        self.name = name
        self.discover_xp = discover_xp
        self.discovery_chance = chance
        self.description = description
        self._activities = {activity.name: activity for activity in activities}
    
    @property
    def activities(self) -> Dict[str, "Activity"]:
        return self._activities

    def examine(self):
        description = f"{self.name.upper()}:\n{self.description}\nActivities:\n"
        for activity_name, activity in self._activities.items():
            description += f" - {activity_name} (min. lvl. {activity.level_requirement} " \
                           f"{activity.main_skill.name}): {activity.description}\n"
        lazy_utility.message(description[:-1])  # remove last newline


class Activity(Simulation):
    def __init__(
        self,
        name: str,
        main_skill: skills.Skill,
        base_weight: float,
        loot_list: List["Loot"],
        description: str = ""
    ):
        self.name = name
        self._main_skill = main_skill
        self._succes_chance = base_weight
        self._loot_table = {loot: loot.roll_weight for loot in loot_list}
        self._level_requirements = 0  # TODO set this based on the loot to check when moving here
        self.description = description

    @property
    def main_skill(self):
        return self._main_skill

    @property
    def level_requirement(self):
        return self._level_requirements

    def _simulate_roll(
        self,
        xp_dict: Dict[str, int],
        item_dict: DefaultDict[str, int]
    ):
        all_xp = xp_dict[self._main_skill.name]
        additional_skill_chance = self._main_skill.get_additional_roll_chance(all_xp)
        main_skill_level = skills.get_level(self._main_skill.name)
        if random.random() < self._succes_chance + additional_skill_chance:
            elligable_loots = {loot: chance for loot, chance in self._loot_table.items() if
                               loot.required_level <= main_skill_level}
            loot = random.choices(list(elligable_loots.keys()), list(elligable_loots.values()), k=1)[0]
            loot.add_xp_and_items(xp_dict, item_dict)
            if loot.is_depleted():
                del self._loot_table[loot]

    def examine(self):
        description = f"{self.name.upper()}:\n{self.description}\nAvailable loot:\n"
        for loot in self._loot_table:
            for reward, amnt in loot.item_rewards.items():
                description += f" - {reward.name}: {amnt}\n"
        lazy_utility.message(description[:-1])


class Loot:
    def __init__(
        self,
        item_rewards: Dict[items.Item, int],
        xp_rewards: Dict[skills.Skill, int],
        weight: float,
        required_level: int,
        max_supply: int = None
    ):
        self.roll_weight = weight
        self._item_rewards = item_rewards
        self._xp_rewards = xp_rewards
        self.required_level = required_level  # level needed to be able to loot this based in the main skill of activity
        self._max_supply = max_supply

    @property
    def item_rewards(self):
        return self._item_rewards

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
            xp_dict[skill.name] += self._xp_rewards[skill]
        for item in self._item_rewards:
            item_dict[item.name] += self._item_rewards[item]

        if self._max_supply is not None:
            self._max_supply -= 1
