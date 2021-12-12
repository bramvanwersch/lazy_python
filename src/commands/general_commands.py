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


def examine(*args):
    current_user_dir = utility.active_user_dir()

    utility.message("Please select if you want to examine an Area a Location or an Activity")
    answer = utility.ask_answer("Invalid answer given. Please choose one of 'Area', 'A', 'Location', 'L', 'Activity',"
                                " 'C'", {"area": 1, "a": 1, "location": 2, "l": 2, "activity": 3, "c": 3},
                                False)
    indexes = ["area", "location", "activity"]
    selected = None
    for index in range(answer):
        if index == 0:
            user_area_dir = current_user_dir / constants.USER_AREA_DIR
            area_files = user_area_dir.glob("*")
            names = [p.name for p in area_files]
        elif index == 1:
            names = areas.get_unlocked_locations(selected)
        else:
            names = ""
        utility.message(f"Please provide the name of the {indexes[index]}")
        selected_value = utility.ask_answer(f"Please choose one of: {', '.join(names)}",
                                            {name: name for name in names}, False)
        selected = selected_value
    selected for if in is

#    utility.ask_answer()


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


GENERAL_COMMANDS = _commands.Command("general", description="General commands that are used to do general account"
                                                            " related things.")
GENERAL_COMMANDS.add_command("check", check, "Check the current activity and get a report on the gained xp and items.")
GENERAL_COMMANDS.add_command("move", move, "Move to any of the available areas.")
GENERAL_COMMANDS.add_command("examine", examine, "Examine an area, location or activity for some additional information.")
