from typing import Dict, Any

from src import constants


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


def set_values_in_file(file, names, values):
    new_text = []
    with open(file) as f:
        for line in f:
            for index, name in enumerate(names):
                if line.startswith(f"{name}:"):
                    new_text.append(f"{name}:{values[index]}\n")
                else:
                    new_text.append(line)
    with open(file, "w") as f:
        f.write(''.join(new_text))


def message(string):
    print(f"(lazy)> {string}")
