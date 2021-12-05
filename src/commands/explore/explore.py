

from src.commands import commands
from src import utility
from src import constants


def explore_area():
    utility.get_values_from_file(utility.active_user_dir() / constants.USER_GENERAL_FILE_NAME, "")
    utility.message("You are currently in area {}")



EXPLORE_COMMANDS = commands.Command("explore")
EXPLORE_COMMANDS.add_command("area", explore_area, "Choose an area to explore")
