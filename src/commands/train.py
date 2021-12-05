from src.commands import _commands
from src import utility
from src import constants
from src import areas
from src import skills


def explore(*args):
    current_user_dir = utility.active_user_dir()
    current_user_area = utility.get_values_from_file(current_user_dir / constants.USER_GENERAL_FILE_NAME,
                                                     ["current_area"])[0]
    utility.message(f"Started exploring {current_user_area}...")
    utility.set_values_in_file(current_user_dir / constants.USER_GENERAL_FILE_NAME, ["current_activity"], ["exploring"])


TRAINING_COMMANDS = _commands.Command("train", description="The explore command is used to explore areas and move to "
                                                           "new areas")
TRAINING_COMMANDS.add_command("explore", explore, "Explore the current area")
