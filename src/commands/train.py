from src.commands import _commands
from src import utility
from src import constants
from src import areas
from src import skills

from src.commands import general_commands


def explore(*_):
    # special case cant realy be done with _set_training_skill
    general_commands.check()
    current_user_dir = utility.active_user_dir()
    current_user_area = utility.get_values_from_file(current_user_dir / constants.USER_GENERAL_FILE_NAME,
                                                     ["current_area"])[0]
    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["current_activity"],
                               [skills.Skills.EXPLORING.name])
    utility.message(f"Started exploring {current_user_area}...")


def _set_training_skill(skill_name):
    # make sure to check the current activity
    general_commands.check()
    location_obj = areas.get_current_location_object()
    if location_obj is None:
        utility.message("No location currently selected.")
        return
    activity_skills = {activity.main_skill.name for activity in location_obj.activities.values()}
    if skill_name not in activity_skills:
        utility.message(f"Can not train {skill_name} at this location. Choose one of the following: "
                        f"{','.join(activity_skills)}.")
        return
    current_user_dir = utility.active_user_dir()
    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["current_activity"],
                               [skill_name])

    utility.message(f"Started {skill_name} at {location_obj.name}...")


def gather(*_):
    _set_training_skill(skills.Skills.GATHERING.name)


def woodcut(*_):
    _set_training_skill(skills.Skills.WOODCUTTING.name)


def fish(*_):
    _set_training_skill(skills.Skills.FISHING.name)


TRAINING_COMMANDS = _commands.Command("train", description="The train command is used to train various skills. The "
                                                           "skills that can be trained depend on the current area and "
                                                           "location. An area can always be explored to reveal more "
                                                           "locations were other skills can be performed")
TRAINING_COMMANDS.add_command(skills.Skills.EXPLORING.name, explore, "Explore the current area and find new locations "
                                                                     "to perform activities.",
                              f"lazy train {skills.Skills.EXPLORING.name}")
TRAINING_COMMANDS.add_command(skills.Skills.WOODCUTTING.name, woodcut, "Woodcut at the current location",
                              f"lazy train {skills.Skills.WOODCUTTING.name}")
TRAINING_COMMANDS.add_command(skills.Skills.FISHING.name, fish, "Fish at the current location",
                              f"lazy train {skills.Skills.FISHING.name}")
TRAINING_COMMANDS.add_command(skills.Skills.GATHERING.name, gather, "Gather at the current location",
                              f"lazy train {skills.Skills.GATHERING.name}")
