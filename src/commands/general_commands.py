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
    passed_time = float(utility.get_values_from_file(utility.active_user_dir() / constants.USER_GENERAL_FILE_NAME,
                                                     ["last_time_stamp"])[0]) - time.time()

    if constants.TESTING:
        passed_time += 360  # tien minuten

    # TODO report items and xp
    # values are returned in order to report them
    xp_dict, item_dict = area_obj.perform_activity_rolls(location, activity, passed_time)

    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["last_time_stamp"],
                               [str(time.time())])


def move(*args):
    # TODO add no input support
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


GENERAL_COMMAND = _commands.Command("general", description="General commands that are used to do general account"
                                                           " related things.")
GENERAL_COMMAND.add_command("check", check, "Check the current activity and get a report on the gained xp and items.")
GENERAL_COMMAND.add_command("move", move, "Check the current activity and get a report on the gained xp and items.")