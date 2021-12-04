from typing import Dict

from src import utility
from src import constants


class Skills:
    EXPLORING = "exploring"
    GATHERING = "gathering"

    @classmethod
    def all_skills(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__")]


def add_xp(xp_dict):
    user_dir = utility.active_user_dir()
    utility.add_values_in_file(user_dir / constants.USER_LEVEL_FILE_NAME, list(xp_dict.keys()),
                               list(xp_dict.values()), int)


def get_levels() -> Dict[str, int]:
    user_dir = utility.active_user_dir()
    level_dict = utility.get_all_named_values_from_file(user_dir / constants.USER_LEVEL_FILE_NAME, int)
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
