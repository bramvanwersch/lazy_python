from typing import Dict
from abc import ABC

from src import utility
from src import constants


class Skill(ABC):
    # skills give an additional roll chance
    def __init__(self, name):
        self.name = name

    def get_additional_roll_chance(self, xp):
        level = xp_to_level(xp)
        # TODO: think about changing per level with a formula
        return level * 0.005


def add_xp(xp_dict):
    user_dir = utility.active_user_dir()
    utility.add_values_in_file(user_dir / constants.USER_LEVEL_FILE_NAME, list(key.name for key in xp_dict.keys()),
                               list(xp_dict.values()), int)


def get_xps() -> Dict[str, int]:
    user_dir = utility.active_user_dir()
    level_dict = utility.get_all_named_values_from_file(user_dir / constants.USER_LEVEL_FILE_NAME, int)
    return level_dict


def get_xp(name: str) -> int:
    user_dir = utility.active_user_dir()
    return int(utility.get_values_from_file(user_dir / constants.USER_LEVEL_FILE_NAME, [name])[0])


def get_levels() -> Dict[str, int]:
    level_dict = get_xps()
    for name in level_dict:
        level_dict[name] = xp_to_level(level_dict[name])
    return level_dict


def get_level(name) -> int:
    user_dir = utility.active_user_dir()
    xp = utility.get_values_from_file(user_dir / constants.USER_LEVEL_FILE_NAME, [name])[0]
    return xp_to_level(int(xp))


def xp_to_level(xp: int) -> int:
    for index, value in enumerate(constants.XP_ATLEVEL):
        if value > xp:
            return index
    return len(constants.XP_ATLEVEL)


def level_to_xp(level: int) -> int:
    if level == 0:
        return 0
    return constants.XP_ATLEVEL[level - 1]
