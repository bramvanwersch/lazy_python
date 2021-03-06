from lazy_src.commands.account import ACCOUNT_COMMANDS
from lazy_src.commands.train import TRAINING_COMMANDS
from lazy_src.commands.general_commands import EXAMINE_COMMANDS, MOVE_COMMANDS, CHECK_COMMAND, UPDATE_COMMAND
from lazy_src.commands._commands import *


COMMANDS = {
    ACCOUNT_COMMANDS.name: ACCOUNT_COMMANDS,
    TRAINING_COMMANDS.name: TRAINING_COMMANDS,
    EXAMINE_COMMANDS.name: EXAMINE_COMMANDS,
    MOVE_COMMANDS.name: MOVE_COMMANDS,
    CHECK_COMMAND.name: CHECK_COMMAND,
    UPDATE_COMMAND.name: UPDATE_COMMAND
}
