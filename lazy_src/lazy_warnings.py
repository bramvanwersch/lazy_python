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
    INVALID_LOCATION = "No location with name {location}."
    UNSELECTED_LOCATION = "No location currently selected. Select a location with the move command."
    INVALID_ACTIVITY = "No activity with name {activity}."
    INVALID_ACTIVITY_AT_LOCATION = "Can not train {activity} at this location. Choose one of the following: " \
                                   "{activities}."
    INVALID_ITEM_NAME = "No item with name '{name}' exists."
    TO_LOW_LEVEL = "Level {level} {skill} is required for {value}"


class DevelopLazyWarning:
    # messages not meant for users
    RETRIEVING_UNKNOWN_FILE_VALUE = "Failed to retrieve value {value} from file {file}."
    SETTING_UNKNOWN_FILE_VALUE = "Failed to set value {value}. Not present in file {file}."
    REMOVING_UNKNOWN_FILE_VALUE = "Failed to remove line {value}. Not present in file {file}."


def warn(warning_string, debug_warning=False, **named_formatting):
    if debug_warning:
        if not lazy_constants.DEBUGGING:
            return
    warning_string = warning_string.format(**named_formatting)
    lazy_utility._message(warning_string, lazy_constants.WARNING_COLOR)  # noqa
