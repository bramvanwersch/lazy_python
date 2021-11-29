from pathlib import Path

BANNED_CHARACTERS = ('"', "'", ":", ";", "\\", "/", "%")


_secret_path = Path(__file__).resolve().parent / "secret"
GENERAL_INFO_PATH = _secret_path / "general.txt"
ACCOUNT_PATH = _secret_path / "accounts.txt"
USER_DIRS_PATH = _secret_path / "users"
