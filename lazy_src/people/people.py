import random
from abc import ABC, abstractmethod
from typing import Union, Type, Dict, List
import datetime

from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings


# TODO add tests

class Person:
    # person located at a location, can be used to talk to or sell stuff
    __COMPONENT_SPLITTER = ">>>"

    __BEHAVIOUR_NAME = "BEHAVIOUR"
    __STATS_NAME = "STATS"
    __TIME_PATTERNS_NAME = "TIME_PATTERNS"

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._response_tree = None  # set while reading person file
        self._time_activity_table = None  # set while reading person file
        self._read_person_file()

        # make sure that all information was defined or certain issues can happen
        if self._response_tree is None:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_FILE, debug_warning=True,
                               name=self.name, info=self.__BEHAVIOUR_NAME)
        elif self._time_activity_table is None:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_FILE, name=self.name,
                               info=self.__TIME_PATTERNS_NAME)

    def examine(self):
        lazy_utility.message(f"{self.name}: {self.description}")

    def talk(self):
        now = datetime.datetime.now()
        activity = self._time_activity_table.get_current_activity(now.hour)
        self._response_tree.conversate(activity, None)

    def _read_person_file(self):
        person_file = lazy_constants.PERSON_FOLDER / self.name
        if not person_file.exists():
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.MISSING_PERSON_FILE, debug_warning=True,
                               person=self.name)
            return
        with open(person_file) as f:
            text = f.read()
        components = text.split(self.__COMPONENT_SPLITTER)
        self._read_memory()
        for component in components:
            if component == "":
                continue
            elif component.startswith(self.__BEHAVIOUR_NAME):
                self._response_tree = _ResponseTree(component, self.name)
            elif component.startswith(self.__STATS_NAME):
                self._read_stats(component)
            elif component.startswith(self.__TIME_PATTERNS_NAME):
                self._time_activity_table = _TimeActivities(component, self.name)
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.UNKNOWN_PERSON_FILE_SECTION, debug_warning=True,
                                   person=self.name, name=component.split("\n")[0])

    def _read_stats(self, text):
        pass

    def _read_memory(self):
        # user dependant
        pass


class _ResponseTree:
    # response types
    __SEP = ";"
    __LINE_SEP = "|"

    __ANSWER = "ANSWER"  # user is expected to choose an answer
    __REPLY = ""  # basic type just reply

    __CONDITION_IF = "IF"
    __CONDITION_ELIF = "ELIF"
    __CONDITION_ELSE = "ELSE"

    def __init__(self, text, name):
        self._name = name  # for debugging purposes

        # possible behaviour trees chosen based on a statement that is tested based on memory and activity
        self.logic_paths = self._read_behavior(text)

    def conversate(self, activity, memory):
        # all separate paths all are tested consecutively
        for logic_path in self.logic_paths:
            behaviour_tree = logic_path.get_behaviour_tree(activity, memory)
            # no statement in path satisfied
            if behaviour_tree is None:
                continue
            response_id = "0"
            while response_id != -1:
                response_id = behaviour_tree[response_id].trigger()

    def _read_behavior(self, text):
        # remove the name line
        lines = text.strip().splitlines()[1:]
        behaviour_tree = {}
        logic_paths = []
        current_logic_statement = None
        for line in lines:
            # skip empty lines
            if len(line) == 0:
                continue
            values = line.split(self.__SEP)
            if len(values) == 1:
                if current_logic_statement is not None:
                    current_logic_statement.set_behaviour_tree(behaviour_tree)
                    if current_logic_statement.id == 0:
                        logic_paths.append(current_logic_statement)
                        behaviour_tree = {}
                current_logic_statement = self._read_logic_statement(line, current_logic_statement)
                continue
            elif len(values) == 5:
                number, talk_text, responses, talking_person, response_type = values
            else:
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

        # make sure to save the last statement
        if current_logic_statement is not None:
            if current_logic_statement.id == 0:
                logic_paths.append({current_logic_statement: behaviour_tree})
            current_logic_statement.set_behaviour_tree(behaviour_tree)
        return logic_paths

    def _read_logic_statement(
        self,
        line: str,
        prev_statement: Union["_LogicStatement", None]
    ) -> Union["_LogicStatement", None]:

        values = line.removesuffix(":").split(" ", 1)
        if len(values) == 2:
            keyword, statement = values
        else:
            keyword = values[0]
            statement = ""
        id_ = prev_statement.id if prev_statement is not None else 0
        if keyword == self.__CONDITION_IF:
            id_ = 0
            statement = _LogicStatement(id_, statement, self._name)
        elif keyword == self.__CONDITION_ELIF or keyword == self.__CONDITION_ELSE:
            if keyword == self.__CONDITION_ELIF and statement == "":
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True, name=self._name,
                                   line=line, extra="no statement for elif")
                return None
            id_ += 1
            statement = _LogicStatement(id_, statement, self._name)
            prev_statement.set_next_statement(statement)
        else:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_LINE, debug_warning=True,
                               name=self._name, line=line)
            return None
        return statement

    def _get_response_class(self, response_type) -> Union[Type["_Response"], None]:
        if response_type == self.__ANSWER:
            return _AnswerResponse
        if response_type == self.__REPLY:
            return _ReplyResponse
        lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_RESPONSE_TYPE, debug_warning=True, name=self._name,
                           type=response_type)
        return None


class _LogicStatement:
    # saves chains of elif logic pushing to the next statement if statement evaluates to false
    person: str
    id: int
    _statement_connector: str
    _statement_parts: List[List[str]]
    _next_statement: Union[None, "_LogicStatement"]
    _behaviour_tree: Union[None, Dict[int, "_Response"]]

    __ACTIVITY_NAME = "ACTIVITY"
    __MEMORY_NAME = "MEMORY"

    __INVERSE = "NOT"
    __AND = "AND"
    __OR = "OR"
    __BIGGER_THEN = ">"
    __SMALLER_THEN = "<"

    def __init__(self, id_, statement, person):
        self.person = person
        self.id = id_
        self._statement_connector = self.__OR
        self._statement_parts = self._read_statement(statement)

        self._next_statement = None  # next logic statment on evaluating false, degfault is no next statement
        self._behaviour_tree = None

    def _read_statement(self, statement: str):
        statment_values = statement.strip().split()
        statement_parts = []
        current_statement = []
        for value in statment_values:
            if value in (self.__AND, self.__OR):
                if self._statement_connector is None:
                    self._statement_connector = value
                elif self._statement_connector != value:
                    lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True,
                                       name=self.person, line=statement, extra="Cannot mix statement connectors")
                    break
                if len(current_statement) > 0:
                    statement_parts.append(current_statement)
                    current_statement = []
            else:
                current_statement.append(value)
        if len(current_statement) > 0:
            statement_parts.append(current_statement)
        return statement_parts

    def get_behaviour_tree(self, activity, memory) -> Union[Dict[int, "_Response"], None]:
        if len(self._statement_parts) == 0:  # the else statemnt
            return self._behaviour_tree

        for statement in self._statement_parts:
            invert_statement = False
            statement_value = False
            for statement_part in statement:
                if statement_part == self.__INVERSE:
                    invert_statement = not invert_statement
                elif statement_part.startswith(self.__ACTIVITY_NAME):
                    statement_value = statement_part.split(".")[1] == activity
                elif statement_part.startswith(self.__MEMORY_NAME):
                    pass  # needs implementation depending on memory
            if invert_statement:
                statement_value = not statement_value
            if self._statement_connector == self.__OR:
                if statement_value:
                    return self._behaviour_tree
                elif self._next_statement is not None:
                    return self._next_statement.get_behaviour_tree(activity, memory)
                else:
                    return None
            else:
                if not statement_value:
                    if self._next_statement is not None:
                        return self._next_statement.get_behaviour_tree(activity, memory)
                    else:
                        return None
        if self._statement_connector == self.__AND:
            return self._behaviour_tree
        return None

    def set_behaviour_tree(self, behaviour_tree: Dict[int, "_Response"]):
        self._behaviour_tree = behaviour_tree

    def set_next_statement(self, statement: "_LogicStatement"):
        self._next_statement = statement


class _Response(ABC):

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


class _ReplyResponse(_Response):
    # simply reply one or more options without further input

    def get_response_id(self) -> int:
        if self.next_ids is None:
            return -1  # end of conversation
        return random.choice(self.next_ids)


class _AnswerResponse(_Response):
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


class _TimeActivities:
    # track what activity is being performed at a given time by the person

    __HOURS_IN_DAY = 24

    def __init__(self, text, person):
        self.person = person
        self._patterns = self._read_pattern_lines(text)

    def get_current_activity(self, time):
        if len(self._patterns) == 0:
            return None
        if time not in self._patterns:
            return None
        return self._patterns[time]

    def _read_pattern_lines(self, text: str) -> Dict[int, str]:
        lines = text.strip().splitlines()[1:]
        time_dictionary = {}
        prev_time = -1
        for line in lines:
            values = line.strip().split(":")
            if len(values) != 2:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_TIME_PATTERN_LINE, debug_warning=True,
                                   line=line, name=self.person)
                continue
            time, activity = values
            try:
                time = int(time)
            except ValueError:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_TIME, debug_warning=True, time=time,
                                   name=self.person)
                continue
            if time < 0 or time >= self.__HOURS_IN_DAY or prev_time >= time:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_TIME, debug_warning=True, time=time,
                                   name=self.person)
                continue

            # since time goes from low to high
            for time in range(time, self.__HOURS_IN_DAY):
                time_dictionary[time] = activity
        return time_dictionary
