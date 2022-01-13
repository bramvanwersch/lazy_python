import random
from abc import ABC, abstractmethod
from typing import Union, Type

from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings


class Person:
    # person located at a location, can be used to talk to or sell stuff

    __BEHAVIOUR_NAME = "BEHAVIOUR"
    __STATS_NAME = "STATS"
    __TIME_PATTERNS_NAME = "TIME_PATTERNS"

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._response_tree = None  # set while reading person file
        self._read_person_file()

    def examine(self):
        lazy_utility.message(f"{self.name}: {self.description}")

    def talk(self):
        self._response_tree.conversate()

    def _read_person_file(self):
        person_file = lazy_constants.PERSON_FOLDER / self.name
        if not person_file.exists():
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.MISSING_PERSON_FILE, debug_warning=True,
                               person=self.name)
            return
        with open(person_file) as f:
            text = f.read()
        components = text.split(">")
        self._read_memory()
        for component in components:
            if component.startswith(self.__BEHAVIOUR_NAME):
                self._response_tree = ResponseTree(component, self.name)
            elif component.startswith(self.__STATS_NAME):
                self._read_stats(component)
            elif component.startswith(self.__TIME_PATTERNS_NAME):
                self._read_time_patterns(component)
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning, debug_warning=True, person=self.name,
                                   name=component.split("\n")[0])

    def _read_stats(self, text):
        pass

    def _read_time_patterns(self, text):
        pass

    def _read_memory(self):
        # user dependant
        pass


class ResponseTree:
    # response types
    __SEP = ";"
    __LINE_SEP = "|"

    __ANSWER = "ANSWER"  # user is expected to choose an answer
    __REPLY = ""  # basic type just reply

    def __init__(self, text, name):
        self._name = name  # for debugging purposes
        self.tree = self._read_behavior(text)

    def conversate(self):
        response_id = "0"
        while response_id != -1:
            response_id = self.tree[response_id].trigger()

    def _read_behavior(self, text):
        # remove the name line
        lines = text.strip().split("\n")[1:]
        behaviour_tree = {}
        for line in lines:
            # skip empty lines
            if len(line) == 0:
                continue
            try:
                number, talk_text, responses, talking_person, response_type = line.split(self.__SEP)
            except ValueError:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_LINE, debug_warning=True,
                                   name=self._name, line=line)
                continue
            talk_lines = talk_text.split(self.__LINE_SEP)
            if talking_person == "":
                talking_person = self._name
            response_class = self._get_response_class(response_type)
            if response_class is None:
                continue
            behaviour_tree[number] = response_class(number, talk_lines, responses, talking_person)
        return behaviour_tree

    def _get_response_class(self, response_type) -> Union[Type["Response"], None]:
        if response_type == self.__ANSWER:
            return AnswerResponse
        if response_type == self.__REPLY:
            return ReplyResponse
        lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_RESPONSE_TYPE, debug_warning=True, name=self._name,
                           type=response_type)
        return None


class Response(ABC):

    def __init__(self, id_, talk_lines, responses, person):
        self.id = id_
        self.next_ids = self._disect_response_ids(responses)
        self.text = self._prepare_lines(talk_lines)
        self.person = person

    def _prepare_lines(self, lines: str) -> str:
        return '\n'.join(lines)

    def _disect_response_ids(self, responses):
        if responses == "":
            return None
        numbers = responses.split()
        return numbers

    def trigger(self) -> int:
        continue_last = False if self.id == 0 else True
        if self.text != "":
            lazy_utility.message_person(self.text, self.person, continue_last=continue_last)
        return self.get_response_id()

    @abstractmethod
    def get_response_id(self) -> int:
        pass


class ReplyResponse(Response):
    # simply reply one or more options without further input

    def get_response_id(self) -> int:
        if self.next_ids is None:
            return -1  # end of conversation
        return random.choice(self.next_ids)


class AnswerResponse(Response):
    # expect an answer from the user
    def __init__(self, id_, lines, responses, person):
        self._total_answers = 0
        super().__init__(id_, lines, responses, person)

    def trigger(self) -> int:
        continue_last = False if self.id == 0 else True
        lazy_utility.message(f"choose one of:\n{self.text}", continue_last=continue_last,
                             color=lazy_constants.CONVERSATION_COLOR)
        return self.get_response_id()

    def get_response_id(self) -> int:
        return lazy_utility.ask_answer(
            f"Invalid answer choose one of {', '.join(map(str, range(1, self._total_answers + 1)))}",
            {str(index+1): self.next_ids[index] for index in range(self._total_answers)})

    def _prepare_lines(self, lines: str) -> str:
        formatted_text = ""
        self._total_answers = len(lines)
        if self._total_answers <= 1:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning, debug_warning=True)
        for index, response in enumerate(lines):
            formatted_text += f"  [{index + 1}] {response}\n"
        return formatted_text[:-1]  # remove last newline
