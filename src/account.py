import os

from src import commands
from src import utility
from src import constants


def new():
    utility.message("Please provide username: ")
    while True:
        username = utility.ask_valid_string()
        if _get_username_password(username) == (None, None):
            break
        utility.message(f"Username '{username}' is already in use. Please choose another one:")
    utility.message("Please provide password: ")
    password = utility.ask_valid_string()

    utility.message("Please retype the password to confirm or type 'Cancel' to abbort account creation: ")
    if _confirm_password(password) is False:
        return
    _create_account(username, password)
    utility.message(f"Account succesfully created. Welcome {username}!")

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
    open(active_user_dir / "general.txt", "w").close()
    open(active_user_dir / "levels.txt", "w").close()


def load():
    utility.message("Please provide username: ")
    username = utility.ask_valid_string()
    db_name, db_password = _get_username_password(username)
    if db_name is None:
        utility.message(f"Account with username '{username}' does not exist.")
        return

    utility.message("Please provide password:")
    if _confirm_password(db_password) is False:
        return

    utility.set_values_in_file(constants.GENERAL_INFO_PATH, ["active_user"], [username])

    utility.message(f"Account {username} is now active!")


def info():
    active_user = utility.get_values_from_file(constants.GENERAL_INFO_PATH, ["active_user"])[0]
    utility.message(f"The current active account is: {active_user}")


def delete():
    utility.message("Is not implemented yet :(")
    pass


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


ACCOUNT_COMMANDS = commands.Command("account")
ACCOUNT_COMMANDS.add_command("new", new, "Create a new account")
ACCOUNT_COMMANDS.add_command("load", load, "Load an existing account")
ACCOUNT_COMMANDS.add_command("info", info, "Show some basic information about the current account")
ACCOUNT_COMMANDS.add_command("delete", delete, "Delete an existing account")
