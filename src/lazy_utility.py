from typing import Dict, Any, List, TYPE_CHECKING, Union
import sys

from src import lazy_constants
from src import lazy_warnings

if TYPE_CHECKING:
    from pathlib import Path


class LazyException(Exception):
    pass


def ask_answer(fail_message: str, possible_answers: Dict[str, Any], case_sensitive: bool = True):
    if not case_sensitive:
        possible_answers = {answer.lower(): return_value for answer, return_value in possible_answers.items()}
    while True:
        answer = input()
        if not case_sensitive:
            answer = answer.lower()
        if answer in possible_answers:
            return possible_answers[answer]
        message_question(fail_message)


def ask_valid_string():
    while True:
        answer = input()
        if is_valid_string(answer) is True:
            return answer
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_STRING)


def is_valid_string(string: str):
    # check string for illegals
    if len(string) == 0:
        return False
    for char in string:
        if char in lazy_constants.BANNED_CHARACTERS:
            return False
    return True


def append_to_file(file: Union[str, "Path"], information):
    with open(file, "a") as f:
        f.write(information)


def set_values_in_file(file: Union[str, "Path"], names: List[str], values: List[str]):
    new_text = []
    uncovered_value_names = {name: values[index] for index, name in enumerate(names)}
    with open(file) as f:
        for line in f:
            added_line = False
            for name, value in uncovered_value_names.items():
                if line.startswith(f"{name}:"):
                    new_text.append(f"{name}:{value}\n")
                    uncovered_value_names.pop(name)
                    added_line = True
                    break
            if not added_line:
                new_text.append(line)
    with open(file, "w") as f:
        f.write(''.join(new_text))


def add_values_in_file(file: Union[str, "Path"], names: List[str], values: List[Any], value_type: Any):
    # add values to the current values in the file or add them if not present
    uncovered_value_names = {name: value_type(values[index]) for index, name in enumerate(names)}
    new_text = []
    with open(file) as f:
        for line in f:
            added_line = False
            for name, value in uncovered_value_names.items():
                if line.startswith(f"{name}:"):
                    current_value = value_type(line.replace(f"{name}:", "").strip())
                    new_text.append(f"{name}:{value + current_value}\n")
                    uncovered_value_names.pop(name)
                    added_line = True
                    break
            if not added_line:
                new_text.append(line)
    for name, value in uncovered_value_names.items():
        new_text.append(f"{name}:{value}\n")
    with open(file, "w") as f:
        f.write(''.join(new_text))


def get_values_from_file(file: Union[str, "Path"], names: List[str], value_type: Any = str) -> List[str]:
    values = []
    uncovered_names = {name: None for name in names}
    with open(file) as f:
        for line in f:
            for index, name in enumerate(uncovered_names):
                if line.startswith(f"{name}:"):
                    values.append(value_type(line.replace(f"{name}:", "").strip()))
                    uncovered_names.pop(name)
                    break
            if len(uncovered_names) == 0:
                break
    return values


def get_all_named_values_from_file(file: Union[str, "Path"], value_type: Any = str):
    # convenience function so the names of values are not required
    values = {}
    with open(file) as f:
        for line in f:
            name, value = line.strip().split(":")
            values[name] = value_type(value)
    return values


def remove_lines_from_file(file: Union[str, "Path"], lines: List[str]):
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


def active_user_dir(username: Union[None, str] = None) -> "Path":
    if username is None:
        username = get_values_from_file(lazy_constants.GENERAL_INFO_PATH, [lazy_constants.FILE_GENERAL_ACTIVE_USER])[0]
    if username == "":
        lazy_warnings.warn(lazy_warnings.LazyWarningMessages.NO_USER)
        sys.exit(0)
    return lazy_constants.USER_DIRS_PATH / username


def active_user_area_dir(username: Union[None, str] = None) -> "Path":
    return active_user_dir(username) / lazy_constants.USER_AREA_DIR


def message(string):
    _message(string)


def message_question(string):
    _message(string, lazy_constants.QUESTION_COLOR)


def _message(string, color=''):
    for index, line in enumerate(string.split("\n")):
        if index == 0:
            print(f"(lazy)> {color}{line}")
        else:
            print(f"(....)> {color}{line}")
