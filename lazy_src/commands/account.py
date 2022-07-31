import os
import shutil
import time

from lazy_src.commands import _commands
from lazy_src import lazy_utility
from lazy_src import lazy_constants
from lazy_src import skills
from lazy_src import lazy_warnings
from lazy_src import items


def new(*args):
    # function works with asking the user inputs or by pre-typing out the answers

    # ask username
    input_username_present = len(args) > 0
    if not input_username_present:
        lazy_utility.message("Please provide username: ")
    while True:
        if input_username_present:
            username = args[0]
            if not lazy_utility.is_valid_string(username):
                lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)
                return
        else:
            username = lazy_utility.ask_valid_string()
        if _get_username_password(username) == (None, None):
            break
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.DOUBLE_USERNAME, username=username)
        lazy_utility.message_question(f"Please choose another one:")
        if input_username_present:
            return

    # ask password
    input_password_present = len(args) > 2
    if input_password_present:
        password = args[1]
        if not lazy_utility.is_valid_string(password):
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)
            return
        if password != args[2]:
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_MATCHING_PASSWORDS)
            return
    else:
        lazy_utility.message_question("Please provide password: ")
        password = lazy_utility.ask_valid_string()
        lazy_utility.message_question("Please retype the password to confirm or type 'Cancel' to abbort "
                                      "account creation: ")
        if _confirm_password(username, password) is False:
            return
    _create_account(username, password)
    lazy_utility.message(f"Account succesfully created. Welcome {username}!")
    if input_password_present:
        return
    # ask user to activate account
    lazy_utility.message("Do you want to activate the new account? [Y/N]")
    answer = lazy_utility.ask_answer("Please answer one of: Y, y, yes, N, n, no", {"Y": True, "y": True, "yes": True,
                                                                                   "N": False, "n": False, "no": False})
    if answer is True:
        lazy_utility.set_values_in_file(lazy_constants.GENERAL_INFO_PATH, [lazy_constants.FILE_GENERAL_ACTIVE_USER],
                                        [username])


def _create_account(
    username: str,
    password: str
):
    lazy_utility.append_to_file(lazy_constants.ACCOUNT_PATH, f"n:{username}\np:{password}\n")
    os.mkdir(lazy_constants.USER_DIRS_PATH / username)
    active_user_dir = lazy_utility.active_user_dir(username)

    # write general file values
    with open(active_user_dir / lazy_constants.USER_GENERAL_FILE_NAME, "w") as f:
        f.write(f"{lazy_constants.USERFILE_GENERAL_CURRENT_AREA}:{lazy_constants.STARTING_AREA}\n")
        f.write(f"{lazy_constants.USERFILE_GENERAL_CURRENT_LOCATION}:{lazy_constants.STARTING_LOCATION}\n")
        f.write(f"{lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY}:\n")
        f.write(f"{lazy_constants.USERFILE_GENERAL_TIMESTAMP}:{time.time()}\n")

    # write all the levels
    with open(active_user_dir / lazy_constants.USER_LEVEL_FILE_NAME, "w") as f:
        for skill in skills.Skills.all_skills():
            f.write(f"{skill.name}:0\n")

    # create inventory
    with open(active_user_dir / lazy_constants.USER_INVENTORY_FILE_NAME, "w") as f:
        f.write("")

    # for saving area specific information
    os.mkdir(active_user_dir / lazy_constants.USER_AREA_DIR)
    create_area_file(lazy_constants.STARTING_AREA, username, [lazy_constants.STARTING_LOCATION])

    # create equiped item file
    with open(active_user_dir / lazy_constants.USER_EQUIPMENT_FILE_NAME, "w") as f:
        for slot in items.WearableItem.all_equipment_slots():
            f.write(f"{slot}:\n")


def create_area_file(area_name, username=None, unlocked_areas=None):
    # put all area specific values in this file. Set expected defined values here
    with open(lazy_utility.active_user_area_dir(username) / area_name, "w") as f:
        f.write(f"{lazy_constants.USERFILE_AREA_UNLOCKED_LOCATIONS}:"
                f"{'' if unlocked_areas is None else ','.join(unlocked_areas)}\n")


def activate(*args):
    input_username_present = len(args) > 0
    if input_username_present:
        username = args[0]
        if not lazy_utility.is_valid_string(username):
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)
            return
    else:
        lazy_utility.message_question("Please provide username: ")
        username = lazy_utility.ask_valid_string()
    db_name, db_password = _get_username_password(username)
    if db_name is None:
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.UNKNOWN_USERNAME, username=username)
        return

    input_password_provided = len(args) > 1
    if input_password_provided:
        password = args[1]
        if not lazy_utility.is_valid_string(password):
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)
            return
        if password != db_password:
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER_MATCHING_PASSWORD, username=username)
            return
    else:
        lazy_utility.message_question("Please provide password:")
        if _confirm_password(username, db_password) is False:
            return

    lazy_utility.set_values_in_file(lazy_constants.GENERAL_INFO_PATH, ["active_user"], [username])

    lazy_utility.message(f"Account {username} is now active! All commands that convey account specific actions now "
                         f" are applied to this account.")


def info(*args):
    active_user = lazy_utility.get_values_from_file(lazy_constants.GENERAL_INFO_PATH,
                                                    [lazy_constants.FILE_GENERAL_ACTIVE_USER])[0]
    full_message = f"The current active account is: {active_user if active_user != '' else 'No active account'}\n"
    if active_user == '':
        lazy_utility.message(full_message[:-1])
        return
    user_dir = lazy_utility.active_user_dir(active_user)
    if len(args) == 0:
        _show_general_information(user_dir, full_message)
    else:
        # TODO add option to check equipment
        if args[0] == "levels":
            _show_levels(user_dir, full_message)
        elif args[0] == "items":
            _show_inventory(user_dir, full_message)
        else:
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_COMMAND_OPTION, command="lazy account info",
                               options="levels, items")


def equip(*args):
    active_account = lazy_utility.get_values_from_file(lazy_constants.GENERAL_INFO_PATH, ["active_user"])[0]
    if active_account == "":
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER)
        return
    user_dir = lazy_utility.active_user_dir(active_account)
    inventory = items.get_inventory()
    wearable_items = inventory.get_all_of_type_items(items.WearableItem)

    equiped_items = lazy_utility.get_values_from_file(lazy_constants.USER_EQUIPMENT_FILE_NAME,
                                                      items.WearableItem.all_equipment_slots())

    if len(args) == 0:
        lazy_utility.message_question(f"What item do you wish to equip? You have the following equipable items:"
                                      f" {', '.join(item.name for item in wearable_items)}")
        lazy_utility.ask_answer(f"Please select one of: {', '.join(item.name for item in wearable_items)}",
                                {item.name: item for item in wearable_items}, case_sensitive=False)
    # TODO equip items
    # TODO make sure that equipment has effect on training for instance


def _show_general_information(user_dir, full_message):
    current_area, current_location, current_activity, last_time_stamp = \
        lazy_utility.get_values_from_file(user_dir / lazy_constants.USER_GENERAL_FILE_NAME,
                                          [lazy_constants.USERFILE_GENERAL_CURRENT_AREA,
                                           lazy_constants.USERFILE_GENERAL_CURRENT_LOCATION,
                                           lazy_constants.USERFILE_GENERAL_CURRENT_ACTIVITY,
                                           lazy_constants.USERFILE_GENERAL_TIMESTAMP])
    time_since_last_check = int(time.time() - float(last_time_stamp))
    full_message += f"This account is located in area {current_area} "
    if current_location != '':
        full_message += f"at location {current_location} "
    if current_activity != '':
        full_message += f"doing activity {current_activity}.\n"
    full_message += f"Your last activity check was performed {time_since_last_check} seconds ago."
    lazy_utility.message(full_message)


def _show_levels(user_dir, full_message):
    full_message += "Levels:\n"
    infos = []
    with open(user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
        for line in f:
            name, xp = line.strip().split(":")
            level = skills.xp_to_level(int(xp))
            xp_to_next = skills.xp_to_next_level(int(xp))
            infos.append([name, level, xp_to_next])
    infos.sort()
    for skill_info in infos:
        name, level, xp_to_next = skill_info
        full_message += f"{name}: {level} ({xp_to_next} until next)\n"
    lazy_utility.message(full_message[:-1])


def _show_inventory(user_dir, full_message):
    infos = []
    with open(user_dir / lazy_constants.USER_INVENTORY_FILE_NAME) as f:
        for line in f:
            name, total = line.strip().split(":")
            infos.append([name, total])
    infos.sort()
    for item_info in infos:
        name, total = item_info
        full_message += f"{name}: {total}\n"
    lazy_utility.message(full_message[:-1])


def delete(*args):
    input_password_provided = len(args) > 0
    active_account = lazy_utility.get_values_from_file(lazy_constants.GENERAL_INFO_PATH, ["active_user"])[0]
    if active_account == "":
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER)
        return
    if not input_password_provided:
        lazy_utility.message(f"Starting the process for the deletion of the current active account {active_account}")
        lazy_utility.message_question("Please provide the password for this account to confirm the deletion or type "
                                      "'cancel' to cancel. The deletion can not be undone!")

    username, real_pw = _get_username_password(active_account)

    if input_password_provided:
        password = args[0]
        if not lazy_utility.is_valid_string(password):
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)
            return
        if password != real_pw:
            lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER_MATCHING_PASSWORD, username=username)
            return
    else:
        if _confirm_password(username, real_pw) is False:
            return
    lazy_utility.remove_lines_from_file(lazy_constants.ACCOUNT_PATH, [f"n:{active_account}", f"p:{real_pw}"])
    shutil.rmtree(lazy_constants.USER_DIRS_PATH / active_account)
    lazy_utility.set_values_in_file(lazy_constants.GENERAL_INFO_PATH, ["active_user"], [""])
    lazy_utility.message(f"Account {active_account} is no more.")


def _get_username_password(name):
    with open(lazy_constants.ACCOUNT_PATH) as f:
        for line in f:
            if line.startswith("n:"):
                in_file_name = line[2:].strip()
                if in_file_name == name:
                    password = f.readline().replace("p:", "").strip()
                    return name, password
    return None, None


def _confirm_password(username, real_pw):
    while True:
        password = lazy_utility.ask_valid_string()
        if password == 'cancel':
            return False
        if password == real_pw:
            return True
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER_MATCHING_PASSWORD, username=username)
        lazy_utility.message_question("Please try again or type 'cancel' to abort.")


ACCOUNT_COMMANDS = _commands.Command("account", description="Account managing functionalities. If you are new to the "
                                                            "game this is the place to start and create an account.")
ACCOUNT_COMMANDS.add_command("new", new, "Create a new account", "lazy account new (<name> <password> <password>)")
ACCOUNT_COMMANDS.add_command("activate", activate, "Load an existing account", "lazy account load (<name> <password>)")
ACCOUNT_COMMANDS.add_command("info", info, "Show some basic information about the current account. Optionally request"
                                           " more detailed information with items or levels",
                             "lazy account info (levels | items)")
ACCOUNT_COMMANDS.add_command("equip", equip, "Equip items in the inventory of the current account",
                             "lazy account equip (<itemname>)")
ACCOUNT_COMMANDS.add_command("delete", delete, "Delete the current active account", "lazy account delete (<password>)")
