import os
import shutil
import time

from src.commands import _commands
from src import utility
from src import constants
from src.skills import Skills


def new(*args):
    # function works with asking the user inputs or by pre-typing out the answers

    # ask username
    input_username_present = len(args) > 0
    if not input_username_present:
        utility.message("Please provide username: ")
    while True:
        if input_username_present:
            username = args[0]
            if not utility.is_valid_string(username):
                utility.message(constants.LazyWarningMessages.INVALID_STRING)
                return
        else:
            username = utility.ask_valid_string()
        if _get_username_password(username) == (None, None):
            break
        utility.message(f"Username '{username}' is already in use. Please choose another one:")
        if input_username_present:
            return

    # ask password
    input_password_present = len(args) > 2
    if input_password_present:
        password = args[1]
        if not utility.is_valid_string(password):
            utility.message(constants.LazyWarningMessages.INVALID_STRING)
            return
        if password != args[2]:
            utility.message("Given and repeated password do not match")
            return
    else:
        utility.message("Please provide password: ")
        password = utility.ask_valid_string()
        utility.message("Please retype the password to confirm or type 'Cancel' to abbort account creation: ")
        if _confirm_password(password) is False:
            return
    _create_account(username, password)
    utility.message(f"Account succesfully created. Welcome {username}!")
    if input_password_present:
        return
    # ask user to activate account
    utility.message("Do you want to activate the new account? [Y/N]")
    answer = utility.ask_answer("Please answer one of: Y, y, yes, N, n, no", {"Y": True, "y": True, "yes": True,
                                                                              "N": False, "n": False, "no": False})
    if answer is True:
        utility.set_values_in_file(constants.GENERAL_INFO_PATH, ["active_user"], [username])


def _create_account(username, password):
    utility.append_to_file(constants.ACCOUNT_PATH, f"n:{username}\np:{password}\n")
    os.mkdir(constants.USER_DIRS_PATH / username)
    active_user_dir = utility.active_user_dir(username)
    with open(active_user_dir / constants.USER_GENERAL_FILE_NAME, "w") as f:
        f.write(f"current_area:{constants.STARTING_LOCATION}\n")
        f.write("current_location:\n")
        f.write("current_activity:\n")
        f.write(f"last_time_stamp:{time.time()}\n")
    with open(active_user_dir / constants.USER_LEVEL_FILE_NAME, "w") as f:
        for skill in Skills.all_skills():
            f.write(f"{skill.name}:0\n")
    with open(active_user_dir / constants.USER_INVENTORY_FILE_NAME, "w") as f:
        f.write("")


def load(*args):
    input_username_present = len(args) > 0
    if input_username_present:
        username = args[0]
        if not utility.is_valid_string(username):
            utility.message(constants.LazyWarningMessages.INVALID_STRING)
            return
    else:
        utility.message("Please provide username: ")
        username = utility.ask_valid_string()
    db_name, db_password = _get_username_password(username)
    if db_name is None:
        utility.message(f"Account with username '{username}' does not exist.")
        return

    input_password_provided = len(args) > 1
    if input_password_provided:
        password = args[1]
        if not utility.is_valid_string(password):
            utility.message(constants.LazyWarningMessages.INVALID_STRING)
            return
        if password != db_password:
            utility.message(f"Password does not match the password for {username}")
            return
    else:
        utility.message("Please provide password:")
        if _confirm_password(db_password) is False:
            return

    utility.set_values_in_file(constants.GENERAL_INFO_PATH, ["active_user"], [username])

    utility.message(f"Account {username} is now active!")


def info(*args):
    active_user = utility.get_values_from_file(constants.GENERAL_INFO_PATH, ["active_user"])[0]
    utility.message(f"The current active account is: {active_user if active_user != '' else 'No active account'}")


def delete(*args):
    input_password_provided = len(args) > 0
    active_account = utility.get_values_from_file(constants.GENERAL_INFO_PATH, ["active_user"])[0]
    if active_account == "":
        utility.message(constants.LazyWarningMessages.NO_USER)
        return
    if not input_password_provided:
        utility.message(f"Starting the process for the deletion of the current active account {active_account}")
        utility.message("Please provide the password for this account to confirm the deletion or type cancel "
                        "to cancel. The deletion can not be undone!")

    _, real_pw = _get_username_password(active_account)

    if input_password_provided:
        password = args[0]
        if not utility.is_valid_string(password):
            utility.message(constants.LazyWarningMessages.INVALID_STRING)
            return
        if password != real_pw:
            utility.message(f"Password does not match the password for {active_account}")
            return
    else:
        if _confirm_password(real_pw) is False:
            return
    # TODO: fix issues with the same passwords
    utility.remove_lines_from_file(constants.ACCOUNT_PATH, [f"n:{active_account}", f"p:{real_pw}"])
    shutil.rmtree(constants.USER_DIRS_PATH / active_account)
    utility.set_values_in_file(constants.GENERAL_INFO_PATH, ["active_user"], [""])
    utility.message(f"Account {active_account} is no more.")


def _get_username_password(name):
    with open(constants.ACCOUNT_PATH) as f:
        for line in f:
            if line.startswith("n:"):
                in_file_name = line[2:].strip()
                if in_file_name == name:
                    password = f.readline().replace("p:", "").strip()
                    return name, password
    return None, None


def _confirm_password(real_pw):
    while True:
        password = utility.ask_valid_string()
        if password == 'cancel':
            return False
        if password == real_pw:
            return True
        utility.message("Invalid password provided. Please try again or type 'cancel' to abort.")


ACCOUNT_COMMANDS = _commands.Command("account", description="Account managing functionalities. If you are new to the "
                                                            "game this is the place to start and create an account.")
ACCOUNT_COMMANDS.add_command("new", new, "Create a new account. Example: 'lazy account new (<name> <pw> <pw>)'")
ACCOUNT_COMMANDS.add_command("load", load, "Load an existing account. Example: 'lazy account load (<name> <pw>)'")
ACCOUNT_COMMANDS.add_command("info", info, "Show some basic information about the current account. Example:"
                                           " 'lazy account info'")
ACCOUNT_COMMANDS.add_command("delete", delete, "Delete the current active account. Example: 'lazy account delete"
                                               " (<pw>)'")
