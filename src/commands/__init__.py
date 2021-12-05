from src.commands.account import ACCOUNT_COMMANDS
from src.commands.train import TRAINING_COMMANDS
from src.commands.general_commands import CHECK_COMMAND


COMMANDS = {
    ACCOUNT_COMMANDS.name: ACCOUNT_COMMANDS,
    TRAINING_COMMANDS.name: TRAINING_COMMANDS,
    CHECK_COMMAND.name: CHECK_COMMAND
}
