import shutil
import os

from src import constants
from src.commands import account


def setup_test_folder():

    if not constants.TEST_FOLDER.exists():
        os.mkdir(constants.TEST_FOLDER)

    # very important this happens --> might not work with importing we will see
    constants.set_testing_globals()

    # reset / create the test_file
    clear_test_file()


def clear_test_file():
    if constants.TEST_FILE.exists():
        # clear a general test text file
        open(constants.TEST_FILE, "w").close()


def remove_test_folder():
    # remove all files in test folder
    try:
        shutil.rmtree(constants.TEST_FOLDER)
    except IOError:
        pass


def create_test_account():
    if not constants.TEST_FOLDER.exists():
        setup_test_folder()
    account.new("test", "test", "test")
    account.activate("test", "test")


def remove_test_account():
    account.delete("test")
