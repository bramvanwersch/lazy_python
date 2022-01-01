import subprocess
import os
import shutil

from src import constants

# very important this happens before
constants.set_testing_globals()


def setup_test_folder():
    try:
        os.mkdir(constants.TEST_FOLDER)
    except IOError:
        pass
    # reset / create the test_file
    clear_test_file()


def clear_test_file():
    # clear a general test text file
    open(constants.TEST_FILE, "w").close()


def remove_test_folder():
    # remove the test folder and all files in it
    try:
        shutil.rmtree(constants.TEST_FOLDER)
    except IOError:
        pass


def create_test_account():
    process = subprocess.Popen("lazy account new test test test")
    process.wait()
    process = subprocess.Popen("lazy account activate test test")
    process.wait()


def remove_test_account():
    process = subprocess.Popen("lazy account delete test")
    process.wait()
