import shutil
import os

from lazy_src import lazy_constants
from lazy_src.commands import account


def setup_test_folder():

    if not lazy_constants.TEST_FOLDER.exists():
        os.mkdir(lazy_constants.TEST_FOLDER)

    # very important this happens
    lazy_constants.set_testing_globals()

    # reset / create the test_file
    clear_test_file()


def clear_test_file():
    if lazy_constants.TEST_FILE.exists():
        # clear a general test text file
        open(lazy_constants.TEST_FILE, "w").close()


def remove_test_folder():
    # remove all files in test folder
    try:
        shutil.rmtree(lazy_constants.TEST_FOLDER)
    except IOError:
        pass


def create_test_account(activate=True):
    if not lazy_constants.TEST_FOLDER.exists():
        setup_test_folder()
    account.new("test", "test", "test")
    if activate:
        account.activate("test", "test")


def remove_test_account():
    account.delete("test")
