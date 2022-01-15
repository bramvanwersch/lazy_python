from lazy_src.commands import _commands
from lazy_src import lazy_utility
from lazy_src import lazy_constants
from lazy_src import lazy_warnings
from lazy_src import areas
from lazy_src import skills

from lazy_src.commands import general_commands


def explore(*_):
    # special case cant realy be done with _set_training_skill
    general_commands.check()
    current_user_dir = lazy_utility.active_user_dir()
    current_user_area = lazy_utility.get_values_from_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                                          ["current_area"])[0]
    lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME, ["current_activity"],
                                    [skills.Skills.EXPLORING.name])
    lazy_utility.message(f"Started exploring {current_user_area}...")


def _set_training_skill(skill_object):
    skill_name = skill_object.name
    # make sure to check the current activity
    general_commands.check()
    location_obj = areas.get_current_location_object()
    if location_obj is None:
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.UNSELECTED_LOCATION)
        return
    activity_skills = {}
    for activity in location_obj.activities.values():
        skill_name = activity.main_skill.name
        if skill_name in activity_skills:
            activity_skills[skill_name] = min(activity_skills[skill_name], activity.required_level)
        else:
            activity_skills[skill_name] = activity.required_level
    if skill_name not in activity_skills:
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_ACTIVITY_AT_LOCATION, activity=skill_name,
                           activities=','.join(list(s.name for s in activity_skills.keys())))
        return
    current_skill_level = skills.get_level(skill_name)
    if activity_skills[skill_name] > current_skill_level:
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.TO_LOW_LEVEL, level=activity_skills[skill_name],
                           skill=skill_name, value=f"activity {skill_name}")
        return
    current_user_dir = lazy_utility.active_user_dir()
    lazy_utility.set_values_in_file(current_user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                    [lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY], [skill_name])

    lazy_utility.message(f"Started {skill_name} at {location_obj.name}...")


def gather(*_):
    _set_training_skill(skills.Skills.GATHERING)


def woodcut(*_):
    _set_training_skill(skills.Skills.WOODCUTTING)


def fish(*_):
    _set_training_skill(skills.Skills.FISHING)


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
