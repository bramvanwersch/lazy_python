from typing import Union
import time
import subprocess

from lazy_src.commands import _commands
from lazy_src import lazy_utility
from lazy_src import lazy_constants
from lazy_src import areas
from lazy_src import skills
from lazy_src import items


def check(continue_last=False):
    current_user_dir = lazy_utility.active_user_dir()
    area, location, activity = lazy_utility.get_values_from_file(
        current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
        [lazy_constants.USERFILE_GENERAL_CURRENT_AREA, lazy_constants.USERFILE_GENERAL_CURRENT_LOCATION,
         lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY])
    if area == '' or (location == '' and activity != "exploring") or activity == '':
        lazy_utility.message("Nothing to check yet.", continue_last=continue_last)
        return
    area_obj = areas.AREA_MAPPING[area]
    passed_time = int(time.time() - float(lazy_utility.get_values_from_file(
        lazy_utility.active_user_dir() / lazy_constants.USER_GENERAL_FILE_NAME,
        [lazy_constants.USERFILE_GENERAL_TIMESTAMP])[0]))

    if lazy_constants.TESTING:
        passed_time += 3600  # 60 rolls when testing

    before_check_levels = skills.get_levels()

    check_message = ""
    # values are returned in order to report them
    check_message += f"In total {passed_time}s passed\n"
    xp_dict, item_dict = area_obj.perform_activity_rolls(location, activity, passed_time)
    check_message += "The following things happened while you where away:"
    lazy_utility.message(check_message, continue_last=continue_last)

    gathered_message = ""
    current_xps = skills.get_xps()
    skills.set_xp(xp_dict)
    for skill_name, xp in xp_dict.items():
        xp_difference = xp - current_xps[skill_name]
        if xp_difference <= 0:
            continue
        current_level = skills.xp_to_level(xp)
        level_change = current_level - before_check_levels[skill_name]
        level_str = f"({before_check_levels[skill_name]}-{current_level})" if level_change > 0 else ''
        gathered_message += f"{skill_name}: +{xp_difference}xp {level_str}\n"
    if activity == skills.Skills.EXPLORING.name:
        for location_name, amnt in item_dict.items():
            gathered_message += f"You discovered {location_name}\n"
    else:
        # exploring does not return items but locations
        items.add_items(item_dict)
        for item_name, amnt in item_dict.items():
            if amnt == 1:
                gathered_message += f"You found {item_name}\n"
            else:
                gathered_message += f"You found {amnt} X {item_name}\n"

    lazy_utility.message_loot(gathered_message[:-1], continue_last=True)
    # set the time stamp
    lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                    [lazy_constants.USERFILE_GENERAL_TIMESTAMP], [str(time.time())])


CHECK_COMMAND = _commands.Command("check", self_command=check,
                                  description="Check on the current activity and collect all xp and resources. After"
                                              " that continue. Example: 'lazy check'")


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
            selected_obj = _get_area(*args)
        elif index == 1:
            selected_obj = _get_location(selected_obj, *args)
        else:
            selected_obj = _get_activity(selected_obj, *args)
        if selected_obj is None:
            return
    selected_obj.examine()


EXAMINE_COMMANDS = _commands.Command("examine", description="Examine an area, location or activity to get more detailed"
                                                            " information.")
EXAMINE_COMMANDS.add_command("area", examine_area, "See al the unlocked locations and what there is still to uncover in"
                                                   "an area", "lazy examine area (<area name>)")
EXAMINE_COMMANDS.add_command("location", examine_location,
                             "See all possible activities in a location and all the level requirements",
                             "lazy examine location (<area name> <location name>)")
EXAMINE_COMMANDS.add_command("activity", examine_activity, "Check the loot that you can get from a certain activity.",
                             "lazy examine location (<area name> <location name> <activity name>)")


def _get_area(*args) -> Union[areas.Area, None]:
    current_user_dir = lazy_utility.active_user_dir()
    user_area_dir = current_user_dir / lazy_constants.USER_AREA_DIR
    area_files = user_area_dir.glob("*")
    area_names = [p.name for p in area_files]
    if len(args) >= 1:
        if args[0] in area_names:
            selected_value = args[0]
        else:
            lazy_utility.message(f"No area with name {args[0]}.")
            return None
    else:
        lazy_utility.message(f"Please choose one of the following areas: {', '.join(area_names)}")
        selected_value = lazy_utility.ask_answer(f"Please choose one of: {', '.join(area_names)}",
                                                 {name: name for name in area_names}, False)
    return areas.AREA_MAPPING[selected_value]


def _get_location(area_obj: areas.Area, *args) -> Union[areas.Location, None]:
    location_names = areas.get_unlocked_location_names(area_obj.name)
    if len(args) >= 2:
        if args[1] in location_names:
            selected_value = args[1]
        else:
            lazy_utility.message(f"No location with name {args[1]}.")
            return None
    else:
        lazy_utility.message(f"Please choose one of the following locations: {', '.join(location_names)}")
        selected_value = lazy_utility.ask_answer(f"Please choose one of: {', '.join(location_names)}",
                                                 {name: name for name in location_names}, False)
    return area_obj.locations[selected_value]


def _get_activity(location_obj: areas.Location, *args) -> Union[areas.Activity, None]:
    activity_names = location_obj.activities.keys()
    if len(args) >= 3:
        if args[2] in activity_names:
            selected_value = args[2]
        else:
            lazy_utility.message(f"No activity with name {args[2]}.")
            return None
    else:
        lazy_utility.message(f"Please choose one of the following activities: {', '.join(activity_names)}")
        selected_value = lazy_utility.ask_answer(f"Please choose one of: {', '.join(activity_names)}",
                                                 {name: name for name in activity_names}, False)
    return location_obj.activities[selected_value]


def move_area(*args):
    _move(1, *args)


def move_location(*args):
    _move(2, *args)


def _move(depth, *args):
    # TODO add a moving time or not can be quite annoying
    lazy_utility.message("Before moving the current activity is checked:")
    check()
    # create some separation
    lazy_utility.message("", continue_last=True)

    current_user_dir = lazy_utility.active_user_dir()
    selected_obj: Union[None, areas.Area, areas.Location] = None
    for index in range(depth):
        if index == 0:
            selected_obj = _get_area(*args)
            if selected_obj is None:  # on fail
                return
            lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                            [lazy_constants.USERFILE_GENERAL_CURRENT_AREA], [selected_obj.name])
        else:
            selected_obj = _get_location(selected_obj, *args)
            if selected_obj is None:  # on fail
                return
            lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                            [lazy_constants.USERFILE_GENERAL_CURRENT_LOCATION], [selected_obj.name])

    # make sure to reset the activity after succesfull move
    lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                    [lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY], [""])
    lazy_utility.message(f"You moved to area {selected_obj.name}. You are ready to go do something...")


MOVE_COMMANDS = _commands.Command("move", description="Move to an area to explore or a location to perform skills.")
MOVE_COMMANDS.add_command("area", move_area, "Move to an area in order to explore", "lazy move area (<area name>)")
MOVE_COMMANDS.add_command("location", move_location, "Move to a location in a certain area to perform skills.",
                          "lazy move location (<area name> <location name>)")


def _update():
    popen = subprocess.Popen(f'git --git-dir "{lazy_constants.PROJECT_BASE_PATH / ".git"}" --work-tree '
                             f'"{lazy_constants.PROJECT_BASE_PATH}" pull', shell=True, stdout=subprocess.PIPE)
    stdout, _ = popen.communicate()
    stdout_str = stdout.decode('utf-8')
    if stdout_str.startswith("Already up to date."):
        lazy_utility.message("Nothing to update. Everything is up to date.")
    else:
        lazy_utility.message("A new update has been downloaded and installed.")


UPDATE_COMMAND = _commands.Command("update", self_command=_update,
                                   description="Download the latest update for lazy, this requires git to be installed."
                                               "Example: 'lazy update'")
