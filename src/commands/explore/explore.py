

from src.commands import commands
from src import utility


def explore_area():
    utility.message("What are do you want to explore? Choose one of: ")


EXPLORE_COMMANDS = commands.Command("explore")
EXPLORE_COMMANDS.add_command("area", explore_area, "Choose an area to explore")
