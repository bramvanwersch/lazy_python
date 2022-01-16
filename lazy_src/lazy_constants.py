from pathlib import Path
import os
import appdirs
import colorama

colorama.init()  # this is important for the colouring to work

WARNING_COLOR = colorama.Fore.RED
GREEN_COLOR = colorama.Fore.GREEN
QUESTION_COLOR = colorama.Fore.YELLOW
RESET_COLOR = colorama.Style.RESET_ALL
CONVERSATION_COLOR = colorama.Fore.LIGHTBLUE_EX

# value set when running tests
TESTING = True

# value that can be set to get certain warnings that are not important for the user but are for me
# also enabled during testing
DEBUGGING = True

SHOW_WARN_TRACEBACK = True

# constants for tests
TEST_FOLDER = Path(__file__).resolve().parent.parent / "tests" / "test_dump"
TEST_FILE = TEST_FOLDER / "test_file.txt"

# user warning messages
BANNED_CHARACTERS = ('"', "'", ":", ";", "\\", "/", "%", " ")

# project related data
# path where this project is located for git updating
PROJECT_BASE_PATH = Path(__file__).resolve().parent
# conversation trees of people
PERSON_FOLDER = PROJECT_BASE_PATH / "people" / "people_files"


# user related data
appdata = Path(appdirs.AppDirs().user_data_dir)  # appdata folder
_lazy_appdata_folder = appdata / "lazy"
if not _lazy_appdata_folder.exists():
    os.mkdir(_lazy_appdata_folder)

_data_folder = _lazy_appdata_folder / "data"
GENERAL_INFO_PATH = _data_folder / "general.txt"
ACCOUNT_PATH = _data_folder / "accounts.txt"
USER_DIRS_PATH = _data_folder / "users"

# file name variables
USERFILE_GENERAL_CURRENT_AREA = "current_area"
USERFILE_GENERAL_CURRENT_LOCATION = "current_location"
USERFILE_GENERAL_CURRENT_ACTIVITY = "current_activity"
USERFILE_GENERAL_TIMESTAMP = "last_time_stamp"
USERFILE_AREA_UNLOCKED_LOCATIONS = "unlocked_locations"
FILE_GENERAL_ACTIVE_USER = "active_user"

# ensure the full data folders are present
if not _data_folder.exists():
    os.mkdir(_data_folder)

if not USER_DIRS_PATH.exists():
    os.mkdir(USER_DIRS_PATH)

if not GENERAL_INFO_PATH.exists():
    with open(GENERAL_INFO_PATH, "w") as f:
        f.write(f"{FILE_GENERAL_ACTIVE_USER}:\n")

if not ACCOUNT_PATH.exists():
    open(ACCOUNT_PATH, "w").close()


# user specific files
USER_GENERAL_FILE_NAME = "general.txt"
USER_LEVEL_FILE_NAME = "levels.txt"
USER_INVENTORY_FILE_NAME = "inventory.txt"
USER_AREA_DIR = "areas"
USER_PEOPLE_DIR = "people"

# other
XP_ATLEVEL = (10, 21, 32, 45, 59, 74, 91, 109, 130, 152, 176, 202, 232, 264, 299, 337, 379, 425, 476, 531, 592, 659,
              732, 813, 901, 997, 1103, 1219, 1346, 1485, 1638, 1806, 1990, 2191, 2412, 2655, 2920, 3212, 3531, 3882,
              4266, 4687, 5149, 5655, 6210, 6819, 7486, 8218, 9021, 9900, 10865, 11923, 13083, 14355, 15749, 17279,
              18955, 20793, 22809, 25019, 27443, 30100, 33014, 36208, 39711, 43552, 47764, 52381, 57444, 62996, 69084,
              75758, 83077, 91102, 99900, 109548, 120127, 131726, 144444, 158390, 173681, 190447, 208830, 228987,
              251089, 275323, 301896, 331032, 362979, 398008, 436416, 478531, 524708, 575340, 630858, 691731,
              758478, 831664, 911911, 999901)

# new player values
STARTING_AREA = "green_woods"
STARTING_LOCATION = "home"


def set_testing_globals():
    # adjust globals that define files and point them to different directories that are easily cleaned up
    # this is specifically for testing
    global TESTING, DEBUGGING, GENERAL_INFO_PATH, ACCOUNT_PATH, USER_DIRS_PATH, SHOW_WARN_TRACEBACK
    TESTING = True
    DEBUGGING = True
    SHOW_WARN_TRACEBACK = False  # makes it less spammy

    _test_data_folder = TEST_FOLDER / "data"
    GENERAL_INFO_PATH = _test_data_folder / "general.txt"
    ACCOUNT_PATH = _test_data_folder / "accounts.txt"
    USER_DIRS_PATH = _test_data_folder / "users"

    if not _test_data_folder.exists():
        os.mkdir(_test_data_folder)

    if not USER_DIRS_PATH.exists():
        os.mkdir(USER_DIRS_PATH)

    if not GENERAL_INFO_PATH.exists():
        with open(GENERAL_INFO_PATH, "w") as f:
            f.write(f"{FILE_GENERAL_ACTIVE_USER}:\n")

    if not ACCOUNT_PATH.exists():
        open(ACCOUNT_PATH, "w").close()
