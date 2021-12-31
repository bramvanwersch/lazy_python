import os
import shutil
import time

from src.commands import _commands
from src import utility
from src import constants
from src import skills


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
        f.write(f"current_area:{constants.STARTING_AREA}\n")
        f.write(f"current_location:{constants.STARTING_LOCATION}\n")
        f.write("current_activity:\n")
        f.write(f"last_time_stamp:{time.time()}\n")
    with open(active_user_dir / constants.USER_LEVEL_FILE_NAME, "w") as f:
        for skill in skills.Skills.all_skills():
            f.write(f"{skill.name}:0\n")
    with open(active_user_dir / constants.USER_INVENTORY_FILE_NAME, "w") as f:
        f.write("")

    os.mkdir(active_user_dir / constants.USER_AREA_DIR)
    create_area_file(constants.STARTING_AREA, username, ["home"])


def create_area_file(area_name, username=None, unlocked_areas=None):
    # put all area specific values in this file. Set expected defined values here
    with open(utility.active_user_area_dir(username) / area_name, "w") as f:
        f.write(f"unlocked_locations:{'' if unlocked_areas is None else ','.join(unlocked_areas)}\n")


def activate(*args):
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
    active_user = utility.get_values_from_file(constants.GENERAL_INFO_PATH, [constants.FILE_GENERAL_ACTIVE_USER])[0]
    full_message = f"The current active account is: {active_user if active_user != '' else 'No active account'}\n"
    if active_user == '':
        return
    user_dir = utility.active_user_dir(active_user)
    if len(args) == 0:
        _show_general_information(user_dir, full_message)
    else:
        if args[0] == "levels":
            _show_levels(user_dir, full_message)
        elif args[0] == "inventory":
            _show_inventory(user_dir, full_message)
        else:
            utility.message("Invalid option provided for account info. Expected either 'levels' or 'inventory'.")


def _show_general_information(user_dir, full_message):
    current_area, current_location, current_activity, last_time_stamp = \
        utility.get_values_from_file(user_dir / constants.USER_GENERAL_FILE_NAME,
                                     [constants.USERFILE_GENERAL_CURRENT_AREA,
                                      constants.USERFILE_GENERAL_CURRENT_LOCATION,
                                      constants.USERFILE_GENERAL_CURRENT_ACTIVITY,
                                      constants.USERFILE_GENERAL_TIMESTAMP])
    time_since_last_check = int(time.time() - float(last_time_stamp))
    full_message += f"This account is located in area {current_area} "
    if current_location != '':
        full_message += f"at location {current_location} "
    if current_activity != '':
        full_message += f"doing activity {current_activity}.\n"
    full_message += f"Your last activity check was performed {time_since_last_check} seconds ago"
    utility.message(full_message[:-1])


def _show_levels(user_dir, full_message):
    with open(user_dir / constants.USER_LEVEL_FILE_NAME) as f:
        for line in f:
            name, xp = line.strip().split(":")
            level = skills.xp_to_level(int(xp))
            xp_to_next = skills.xp_to_next_level(int(xp))
            full_message += f"{name}: {level} ({xp_to_next} until next)\n"
    utility.message(full_message[:-1])


def _show_inventory(user_dir, full_message):
    with open(user_dir / constants.USER_INVENTORY_FILE_NAME) as f:
        for line in f:
            name, total = line.strip().split(":")
            full_message += f"{name}: {total}\n"
    utility.message(full_message[:-1])


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
ACCOUNT_COMMANDS.add_command("new", new, "Create a new account", "lazy account new (<name> <password> <password>)")
ACCOUNT_COMMANDS.add_command("activate", activate, "Load an existing account", "lazy account load (<name> <password>)")
ACCOUNT_COMMANDS.add_command("info", info, "Show some basic information about the current account. Optionally request"
                                           " more detailed information with inventory or levels",
                             "lazy account info (levels | inventory)")
ACCOUNT_COMMANDS.add_command("delete", delete, "Delete the current active account", "lazy account delete (<password>)")
