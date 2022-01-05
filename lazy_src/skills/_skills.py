from typing import Dict
from abc import ABC

from lazy_src import lazy_utility
from lazy_src import lazy_constants


class Skill(ABC):
    # skills give an additional roll chance
    def __init__(self, name):
        self.name = name

    def get_additional_roll_chance(self, xp):
        level = xp_to_level(xp)
        # TODO: think about changing per level with a formula
        return level * 0.005


def add_xp(xp_dict):
    user_dir = lazy_utility.active_user_dir()
    lazy_utility.add_values_in_file(user_dir / lazy_constants.USER_LEVEL_FILE_NAME, list(key for key in xp_dict.keys()),
                                    list(xp_dict.values()), int)


def set_xp(xp_dict):
    user_dir = lazy_utility.active_user_dir()
    lazy_utility.set_values_in_file(user_dir / lazy_constants.USER_LEVEL_FILE_NAME, list(key for key in xp_dict.keys()),
                                    list(xp_dict.values()))


def get_xps() -> Dict[str, int]:
    user_dir = lazy_utility.active_user_dir()
    level_dict = lazy_utility.get_all_named_values_from_file(user_dir / lazy_constants.USER_LEVEL_FILE_NAME, int)
    return level_dict


def get_xp(name: str) -> int:
    user_dir = lazy_utility.active_user_dir()
    return int(lazy_utility.get_values_from_file(user_dir / lazy_constants.USER_LEVEL_FILE_NAME, [name])[0])


def get_levels(xps: Dict[str, int] = None) -> Dict[str, int]:
    if xps is None:
        level_dict = get_xps()
    else:
        # make sure not to modify the original
        level_dict = xps.copy()
    for name in level_dict:
        level_dict[name] = xp_to_level(level_dict[name])
    return level_dict


def get_level(name) -> int:
    user_dir = lazy_utility.active_user_dir()
    xp = lazy_utility.get_values_from_file(user_dir / lazy_constants.USER_LEVEL_FILE_NAME, [name])[0]
    return xp_to_level(int(xp))


def xp_to_level(xp: int) -> int:
    for index, value in enumerate(lazy_constants.XP_ATLEVEL):
        if value > xp:
            return index
    return len(lazy_constants.XP_ATLEVEL)


def xp_to_next_level(xp: int) -> int:
    for index, value in enumerate(lazy_constants.XP_ATLEVEL):
        if value > xp:
            return value - xp
    return 0


def level_to_xp(level: int) -> int:
    if level == 0:
        return 0
    return lazy_constants.XP_ATLEVEL[level - 1]
