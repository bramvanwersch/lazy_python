import traceback

from lazy_src import lazy_constants
from lazy_src import lazy_utility


class LazyWarningMessages:
    INVALID_STRING = "Invalid sequence provided. Make sure it contains at least 1 character and does not contain the " \
                     f"following charaters: {' ,'.join(lazy_constants.BANNED_CHARACTERS)}."
    NO_USER = "No user selected. Select a user with 'account activate' or create a new one with 'account new'."
    UNKNOWN_USERNAME = "Account with username '{username}' does not exist."
    DOUBLE_USERNAME = "Username '{username}' is already in use."
    NO_MATCHING_PASSWORDS = "Given and repeated password do not match."
    NO_USER_MATCHING_PASSWORD = "Password does not match the password for '{username}'."
    INVALID_COMMAND_OPTION = "Invalid option provided for {command}. Expected on of: {options}."
    INVALID_AREA = "No area with name {area}."
    UNSELECTED_AREA = "No area currently selected. Select an area with the move command."
    INVALID_LOCATION = "No location with name {location}."
    UNSELECTED_LOCATION = "No location currently selected. Select a location with the move command."
    INVALID_ACTIVITY = "No activity with name {activity}."
    INVALID_ACTIVITY_AT_LOCATION = "Can not train {activity} at this location. Choose one of the following: " \
                                   "{activities}."
    INVALID_ITEM_NAME = "No item with name '{name}' exists."
    TO_LOW_LEVEL = "Level {level} {skill} is required for {value}"

    NO_EQUIPABLE_ITEMS = "You have nothing in your inventory that is not already equiped."
    ITEM_CANNOT_BE_EQUIPED = "Item '{name}' is not in your inventory or is not equipable."


class DevelopLazyWarning:
    # messages not meant for users
    RETRIEVING_UNKNOWN_FILE_VALUE = "Failed to retrieve value {value} from file {file}."
    SETTING_UNKNOWN_FILE_VALUE = "Failed to set value {value}. Not present in file {file}."
    REMOVING_UNKNOWN_FILE_VALUE = "Failed to remove line {value}. Not present in file {file}."

    MISSING_PERSON_FILE = "Person file for {person} is not present."
    UNKNOWN_PERSON_FILE_SECTION = "No file section with name {name} for person {person}."
    INCOMPLETE_PERSON_LINE = "Person {name} encountered an invalid line: {line}."
    INVALID_RESPONSE_TYPE = "No response with type '{type}' for person '{name}'."
    INCOMPLETE_TIME_PATTERN_LINE = "Invalid time_pattern line '{line}' for person '{name}'."
    INVALID_TIME = "Invalid time '{time}' for person '{name}'."
    INCOMPLETE_PERSON_FILE = "Person file for person '{name}' is missing required information: '{info}'"
    INVALID_LOGIC = "Person file for person '{name}' contains invalid logic for line '{line}'. {extra}"

    UNKNOWN_PLAYER_VALUE = "No value with name '{name}' defined for player."

    INVALID_START_IDENTIFIER = "No identifier with name '{identifier}' allowed as start identifier."
    DOUBLE_DATA_ENTRY = "Double data entry with identifier '{identifier}' for person {name}."

    INVALID_ITEM_QUANTITY = "Expected an integer as item quantitiy."

    UNKNOWN_SUBSTITUTE_CONSTANT = "Can not substitute with constant '{constant}'."
    INVALID_SUBSTITUTE_ITEM_AMNT = "Can not convert item amount to integer for person '{name}'"

    INVALID_EQUIPMENT_SLOT = "No equipment slot with name '{name}'"


def warn(warning_string, debug_warning=False, extra_info="", **named_formatting):
    if debug_warning:
        if not lazy_constants.DEBUGGING:
            return
        elif lazy_constants.SHOW_WARN_TRACEBACK:
            traceback.print_stack()
    warning_string = warning_string.format(**named_formatting) + extra_info
    lazy_utility._message(warning_string, lazy_constants.WARNING_COLOR)  # noqa
