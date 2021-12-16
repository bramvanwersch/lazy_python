from typing import Union
import time

from src.commands import _commands
from src import utility
from src import constants
from src import areas
from src import skills


def check():
    current_user_dir = utility.active_user_dir()
    area, location, activity = utility.get_values_from_file(current_user_dir / constants.USER_GENERAL_FILE_NAME,
                                                            ["current_area", "current_location", "current_activity"])
    area_obj = areas.AREA_MAPPING[area]
    passed_time = int(time.time() - float(utility.get_values_from_file(utility.active_user_dir() /
                                                                       constants.USER_GENERAL_FILE_NAME,
                                                                       ["last_time_stamp"])[0]))

    if constants.TESTING:
        passed_time += 3600  # 60 rolls

    before_check_levels = skills.get_levels()

    # values are returned in order to report them
    utility.message(f"In total {passed_time}s passed since last check")
    xp_dict, item_dict = area_obj.perform_activity_rolls(location, activity, passed_time)
    utility.message("The following things happened while you were away:")

    current_levels = skills.get_levels()
    for skill, xp in xp_dict.items():
        level_change = current_levels[skill.name] - before_check_levels[skill.name]
        level_str = f"({before_check_levels[skill.name]}-{current_levels[skill.name]})" if level_change > 0 else ''
        utility.message(f"{skill.name}: +{xp}xp {level_str}")
    if activity == "exploring":
        for item, amnt in item_dict.items():
            utility.message(f"You discovered {item.name}")
    else:
        for item, amnt in item_dict.items():
            if amnt == 1:
                utility.message(f"You found {item.name}")
            else:
                utility.message(f"You found {amnt} X {item.name}")

    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["last_time_stamp"],
                               [str(time.time())])


def examine_area(*args):
    _examine(1, *args)


def examine_location(*args):
    _examine(2, *args)


def examine_activity(*args):
    _examine(3, *args)


def _examine(depth, *args):
    selected_obj = None
    for index in range(depth):
        if index == 0:
            selected_obj = _ask_area(*args)
        elif index == 1:
            selected_obj = _ask_location(selected_obj, *args)
        else:
            selected_obj = _ask_activity(selected_obj, *args)
        if selected_obj is None:
            return
    selected_obj.examine()


EXAMINE_COMMANDS = _commands.Command("examine", description="Examine an area, location or activity to get more detailed"
                                                            "information.")
EXAMINE_COMMANDS.add_command("area", examine_area, "See al the unlocked locations and what there is still to uncover in"
                                                   "an area")
EXAMINE_COMMANDS.add_command("location", examine_location, "See all possible activities in a location and all the "
                                                           "level requirements")
EXAMINE_COMMANDS.add_command("activity", examine_activity, "Check the loot that you can get from a certain activity.")


def _ask_area(*args) -> Union[areas.Area, None]:
    area_names = _get_areas()
    if len(args) >= 1:
        if args[0] in area_names:
            selected_value = args[0]
        else:
            utility.message(f"No area with name {args[0]}.")
            return None
    else:
        utility.message("Please provide the name of the area")
        area_names = _get_areas()
        selected_value = utility.ask_answer(f"Please choose one of: {', '.join(area_names)}",
                                            {name: name for name in area_names}, False)
    return areas.AREA_MAPPING[selected_value]


def _get_areas():
    current_user_dir = utility.active_user_dir()
    user_area_dir = current_user_dir / constants.USER_AREA_DIR
    area_files = user_area_dir.glob("*")
    return [p.name for p in area_files]


def _ask_location(area_obj: areas.Area, *args) -> Union[areas.Location, None]:
    location_names = _get_locations(area_obj)
    if len(args) >= 2:
        if args[1] in location_names:
            selected_value = args[1]
        else:
            utility.message(f"No location with name {args[1]}.")
            return None
    else:
        utility.message("Please provide the name of the location")
        selected_value = utility.ask_answer(f"Please choose one of: {', '.join(location_names)}",
                                            {name: name for name in location_names}, False)
    return area_obj.locations[selected_value]


def _get_locations(area: areas.Area):
    return areas.get_unlocked_locations(area.name)


def _ask_activity(location_obj: areas.Location, *args) -> Union[areas.Activity, None]:
    activity_names = _get_activities(location_obj)
    if len(args) >= 3:
        if args[2] in activity_names:
            selected_value = args[2]
        else:
            utility.message(f"No activity with name {args[2]}.")
            return None
    else:
        utility.message("Please provide the name of the activity")
        selected_value = utility.ask_answer(f"Please choose one of: {', '.join(activity_names)}",
                                            {name: name for name in activity_names}, False)
    return location_obj.activities[selected_value]


def _get_activities(location: areas.Location):
    return location.activities.keys()


def move(*args):
    # TODO add no input support --> also not completely correct
    current_user_dir = utility.active_user_dir()
    current_user_area = utility.get_values_from_file(current_user_dir / constants.USER_GENERAL_FILE_NAME,
                                                     ["current_area"])[0]
    explore_lvl = int(utility.get_values_from_file(current_user_dir / constants.USER_LEVEL_FILE_NAME,
                                                   [skills.Skills.EXPLORING.name])[0])

    utility.message("You can move to any of the following areas: ")
    elligable_areas = areas.Areas.get_elligable_areas(explore_lvl)
    for area in elligable_areas:
        if area.name == current_user_area:
            utility.message(f"-> {area.name}")
        else:
            utility.message(f"   {area.name}")
    utility.message("Choone one of the elligable areas.")
    chosen_area = utility.ask_answer("You can not explore that area or it does not exist. Please choose another",
                                     {area.name: area.name for area in elligable_areas})
    if chosen_area == current_user_area:
        utility.message("That is the same area as you are currenly in. This means that you do not move.")
        return
    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["current_area"], [chosen_area])
    utility.message(f"You moved to area {chosen_area} and start exploring...")
