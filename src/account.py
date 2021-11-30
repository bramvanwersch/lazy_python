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


def _create_account(username, password):
    utility.append_to_file(constants.ACCOUNT_PATH, f"n:{username}\np:{password}\n")
    os.mkdir(constants.USER_DIRS_PATH / username)
    # TODO: make other needed files


def load():
    utility.message("Please provide username: ")
    username = utility.ask_valid_string()
    db_name, db_password = _get_username_password(username)
    if db_name is None:
        utility.message(f"Account with username '{username}' does not exist.")
        return

    utility.set_values_in_file(constants.GENERAL_INFO_PATH, ["active_user"], [username])

    utility.message("Please provide password:")
    if _confirm_password(db_password) is False:
        return

    utility.message(f"Account {username} is now active!")


def delete():
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


ACCOUNT_COMMANDS = commands.Command("new")
ACCOUNT_COMMANDS.add_command("new", new, "Create a new account")
ACCOUNT_COMMANDS.add_command("load", load, "Load an existing account")
ACCOUNT_COMMANDS.add_command("delete", delete, "Delete an existing account")
