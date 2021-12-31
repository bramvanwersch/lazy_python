import subprocess
import os
import shutil

from src import constants


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
    # make sure to safeguard this information before testing affects it
    _save_general_file_information("general", constants.GENERAL_INFO_PATH)
    _save_general_file_information("accounts", constants.ACCOUNT_PATH)

    process = subprocess.Popen("lazy account new test test test")
    process.wait()
    process = subprocess.Popen("lazy account activate test test")
    process.wait()


def _save_general_file_information(temp_file_name, original_file):
    with open(original_file) as f:
        info = f.read()
    with open(constants.TEST_FOLDER / temp_file_name, "w") as f:
        f.write(info)


def remove_test_account():
    process = subprocess.Popen("lazy account delete test")
    process.wait()
    _restore_general_info("general", constants.GENERAL_INFO_PATH)
    _restore_general_info("accounts", constants.ACCOUNT_PATH)


def _restore_general_info(name, path):
    with open(constants.TEST_FOLDER / name) as f:
        info = f.read()

    with open(path, "w") as f:
        f.write(info)
