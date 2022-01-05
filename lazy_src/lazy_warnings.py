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


def warn(warning_string, **named_formatting):
    warning_string = warning_string.format(**named_formatting)
    lazy_utility._message(warning_string, lazy_constants.WARNING_COLOR)  # noqa
