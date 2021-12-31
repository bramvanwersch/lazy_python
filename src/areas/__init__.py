from typing import Union

from src.areas.locations import *
from src.areas.green_woods_area_definitions import green_woods


# easy acces for all areas
class Areas:
    GREEN_WOODS = green_woods

    @classmethod
    def get_elligable_areas(cls, level):
        areas = []
        for area in cls.all_areas():
            if area.required_level <= level:
                areas.append(area)
        return areas

    @classmethod
    def all_areas(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname not in ["all_areas", "get_elligable_areas", "area_by_name"]]


def get_current_area_object() -> Union[None, Area]:
    current_area = utility.get_values_from_file(utility.active_user_dir() /
                                                constants.USER_GENERAL_FILE_NAME, ["current_area"])[0]
    if current_area == '':
        return None
    return AREA_MAPPING[current_area]


def get_current_location_object() -> Union[None, Location]:
    area_obj = get_current_area_object()
    if area_obj is None:
        return None
    current_location = utility.get_values_from_file(utility.active_user_dir() /
                                                    constants.USER_GENERAL_FILE_NAME, ["current_location"])[0]
    if current_location == '':
        return None
    return area_obj.locations[current_location]


def get_current_activity_object() -> Union[None, Activity]:
    location_obj = get_current_location_object()
    if location_obj is None:
        return None
    current_activity = utility.get_values_from_file(utility.active_user_dir() /
                                                    constants.USER_GENERAL_FILE_NAME, ["current_activity"])[0]
    if current_activity == '':
        return None
    return location_obj.activities[current_activity]


AREA_MAPPING: Dict[str, locations.Area] = {area.name: area for area in Areas.all_areas()}
