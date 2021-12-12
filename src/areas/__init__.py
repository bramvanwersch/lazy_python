from typing import Dict

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


AREA_MAPPING: Dict[str, locations.Area] = {area.name: area for area in Areas.all_areas()}
