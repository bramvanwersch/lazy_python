from pathlib import Path

TESTING = True

# constants for tests
TEST_FOLDER = Path(__file__).resolve().parent / "test_dump"
TEST_FILE = TEST_FOLDER / "test_file.txt"

# user warning messages
BANNED_CHARACTERS = ('"', "'", ":", ";", "\\", "/", "%", " ")


class LazyWarningMessages:
    INVALID_STRING = "Invalid sequence provided. Make sure it contains at least 1 character and does not contain the " \
                     f"following charaters: {' ,'.join(BANNED_CHARACTERS)}"
    NO_USER = "No user selected. Select a user with 'account load' or create a new one with 'account new'"


# all user files
_secret_path = Path(__file__).resolve().parent.parent / "data" / "secret"
PROJECT_BASE_PATH = _secret_path.parent.parent
GENERAL_INFO_PATH = _secret_path / "general.txt"
ACCOUNT_PATH = _secret_path / "accounts.txt"
USER_DIRS_PATH = _secret_path / "users"

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

USERFILE_GENERAL_CURRENT_AREA = "current_area"
USERFILE_GENERAL_CURRENT_LOCATION = "current_location"
USERFILE_GENERAL_CURRENT_ACTIVITY = "current_activity"
USERFILE_GENERAL_TIMESTAMP = "last_time_stamp"
FILE_GENERAL_ACTIVE_USER = "active_user"
