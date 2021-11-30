from typing import Dict, Any, List, TYPE_CHECKING, Union

from src import constants

if TYPE_CHECKING:
    import pathlib


class LazyException(Exception):
    pass


def ask_answer(fail_message: str, possible_answers: Dict[str, Any]):
    while True:
        answer = input()
        if answer in possible_answers:
            return possible_answers[answer]
        message(fail_message)


def ask_valid_string():
    while True:
        answer = input()
        if check_string(answer) is True:
            return answer
        message("Invalid sequence provided. Make sure it contains at least 1 character and does not contain the "
                f"following charaters: {' ,'.join(constants.BANNED_CHARACTERS)}")


def check_string(string: str):
    # check string for illegals
    if len(string) == 0:
        return False
    for char in string:
        if char in constants.BANNED_CHARACTERS:
            return False
    return True


def append_to_file(file, information):
    with open(file, "a") as f:
        f.write(information)


def set_values_in_file(file: str, names: List[str], values: List[str]):
    new_text = []
    uncovered_names = {name: None for name in names}
    with open(file) as f:
        for line in f:
            added_line = False
            for index, name in enumerate(uncovered_names):
                if line.startswith(f"{name}:"):
                    new_text.append(f"{name}:{values[index]}\n")
                    uncovered_names.pop(name)
                    added_line = True
                    break
            if not added_line:
                new_text.append(line)
    with open(file, "w") as f:
        f.write(''.join(new_text))


def get_values_from_file(file: str, names: List[str]) -> List[str]:
    values = []
    uncovered_names = {name: None for name in names}
    with open(file) as f:
        for line in f:
            for index, name in enumerate(uncovered_names):
                if line.startswith(f"{name}:"):
                    values.append(line.replace(f"{name}:", "").strip())
                    uncovered_names.pop(name)
                    break
            if len(uncovered_names) == 0:
                break
    return values


def remove_lines_from_file(file: str, lines: List[str]):
    new_text = []
    uncovered_values = {value: None for value in lines}
    with open(file) as f:
        for line in f:
            remove_line = False
            for index, value in enumerate(uncovered_values):
                if line.strip() == value:
                    uncovered_values.pop(value)
                    remove_line = True
                    break
            if not remove_line:
                new_text.append(line)
    with open(file, "w") as f:
        f.write(''.join(new_text))


def active_user_dir(username: Union[None, str] = None) -> "pathlib.Path":
    if username is None:
        username = get_values_from_file(constants.GENERAL_INFO_PATH, ["active_user"])[0]
    return constants.USER_DIRS_PATH / username


def message(string):
    print(f"(lazy)> {string}")
