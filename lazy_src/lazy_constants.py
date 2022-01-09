from pathlib import Path
import os
import appdirs
import colorama

colorama.init()  # this is important for the colouring to work

WARNING_COLOR = colorama.Fore.RED
GREEN_COLOR = colorama.Fore.GREEN
QUESTION_COLOR = colorama.Fore.YELLOW
RESET_COLOR = colorama.Style.RESET_ALL

# value set when running tests
TESTING = False

# value that can be set to get certain warnings that are not important for the user but are for me
# also enabled during testing
DEBUGGING = False

# constants for tests
TEST_FOLDER = Path(__file__).resolve().parent.parent / "tests" / "test_dump"
TEST_FILE = TEST_FOLDER / "test_file.txt"

# user warning messages
BANNED_CHARACTERS = ('"', "'", ":", ";", "\\", "/", "%", " ")


# path where this project is located for git updating
PROJECT_BASE_PATH = Path(__file__).resolve().parent

# all user files
appdata = Path(appdirs.AppDirs().user_data_dir)  # appdata folder
_lazy_appdata_folder = appdata / "lazy"
if not _lazy_appdata_folder.exists():
    os.mkdir(_lazy_appdata_folder)

_data_folder = _lazy_appdata_folder / "data"
_secret_path = _data_folder / "secret"
GENERAL_INFO_PATH = _secret_path / "general.txt"
ACCOUNT_PATH = _secret_path / "accounts.txt"
USER_DIRS_PATH = _secret_path / "users"

# file name varaibles
USERFILE_GENERAL_CURRENT_AREA = "current_area"
USERFILE_GENERAL_CURRENT_LOCATION = "current_location"
USERFILE_GENERAL_CURRENT_ACTIVITY = "current_activity"
USERFILE_GENERAL_TIMESTAMP = "last_time_stamp"
USERFILE_AREA_UNLOCKED_LOCATIONS = "unlocked_locations"
FILE_GENERAL_ACTIVE_USER = "active_user"

# ensure the full data folders are present
if not _data_folder.exists():
    os.mkdir(_data_folder)

if not _secret_path.exists():
    os.mkdir(_secret_path)

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
    global TESTING, DEBUGGING, GENERAL_INFO_PATH, ACCOUNT_PATH, USER_DIRS_PATH
    TESTING = True
    DEBUGGING = True

    _test_data_folder = TEST_FOLDER / "data"
    _test_secret_path = _test_data_folder / "secret"
    GENERAL_INFO_PATH = _test_secret_path / "general.txt"
    ACCOUNT_PATH = _test_secret_path / "accounts.txt"
    USER_DIRS_PATH = _test_secret_path / "users"

    if not _test_data_folder.exists():
        os.mkdir(_test_data_folder)

    if not _test_secret_path.exists():
        os.mkdir(_test_secret_path)

    if not USER_DIRS_PATH.exists():
        os.mkdir(USER_DIRS_PATH)

    if not GENERAL_INFO_PATH.exists():
        with open(GENERAL_INFO_PATH, "w") as f:
            f.write(f"{FILE_GENERAL_ACTIVE_USER}:\n")

    if not ACCOUNT_PATH.exists():
        open(ACCOUNT_PATH, "w").close()
