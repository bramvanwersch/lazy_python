import random
import re
from abc import ABC, abstractmethod
from typing import Union, Type, Dict, List
import datetime

from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings
from lazy_src import items

# TODO add tests
#  Add player stats where player specific values can be requested


STATEMENT_SEP = ";"
COMPONENT_SPLITTER = ">>>"
IGNORE_SYMBOL = "#"

PLAYER_CONST = "PLAYER"
MEMORY_CONST = "MEMORY"
INVENTORY_CONST = "INVENTORY"


def component_lines(data):
    for line in data.strip().splitlines()[1:]:
        if len(line) == 0:
            continue
        if line.startswith(IGNORE_SYMBOL):
            continue
        yield line


class PlayerValues:
    # convenience functions for getting player specific values

    @classmethod
    def name(cls):
        active_user = lazy_utility.get_values_from_file(lazy_constants.GENERAL_INFO_PATH,
                                                        [lazy_constants.FILE_GENERAL_ACTIVE_USER])[0]
        return active_user

    @classmethod
    def money(cls):
        # TODO make actual implementation
        if lazy_constants.TESTING:
            return 100
        raise NotImplemented()

    @classmethod
    def ask_value(cls, value: str):
        if value == "money":
            return cls.money()
        elif value == "name":
            return cls.name()
        else:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.UNKNOWN_PLAYER_VALUE, debug_warning=True, name=value)
        return None


class Person:
    # person located at a location, can be used to talk to or sell stuff
    name: str
    description: str
    _response_tree: Union["_ResponseTree", None]
    _time_activity_table: Union["_TimeActivities", None]
    _character_specific_data: Union["_CharacteSpecificData", None]

    # general defined person behaviour file values
    __BEHAVIOUR_NAME = "BEHAVIOUR"
    __STATS_NAME = "STATS"
    __START_VALUES_NAME = "START"
    __TIME_PATTERNS_NAME = "TIME_PATTERNS"

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._response_tree = None  # set while reading person file
        self._time_activity_table = None  # set while reading person file
        self._character_specific_data = None  # set while reading person file
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

    def talk(self, *args):
        # TODO implement args for non input conversations
        now = datetime.datetime.now()
        activity = self._time_activity_table.get_current_activity(now.hour)
        self._response_tree.conversate(activity)

    def _read_person_file(self):
        person_file = lazy_constants.PERSON_FOLDER / self.name
        if not person_file.exists():
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.MISSING_PERSON_FILE, debug_warning=True,
                               person=self.name)
            return
        with open(person_file) as f:
            text = f.read()
        components = text.split(COMPONENT_SPLITTER)
        # first collect all information
        response_data = ""
        stats_data = ""
        time_activity_data = ""
        starting_data = ""
        for component in components:
            if component == "":
                continue
            elif component.startswith(self.__BEHAVIOUR_NAME):
                response_data = component
            elif component.startswith(self.__STATS_NAME):
                stats_data = component
            elif component.startswith(self.__TIME_PATTERNS_NAME):
                time_activity_data = component
            elif component.startswith(self.__START_VALUES_NAME):
                starting_data = component
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.UNKNOWN_PERSON_FILE_SECTION, debug_warning=True,
                                   person=self.name, name=component.split("\n")[0])
        self._character_specific_data = _CharacteSpecificData(starting_data, self.name)

        self._response_tree = _ResponseTree(response_data, self.name, self._character_specific_data)
        self._read_stats(stats_data)
        self._time_activity_table = _TimeActivities(time_activity_data, self.name)

    def _read_stats(self, text):
        # TODO: implement this
        pass


class _ResponseTree:
    # response types
    __LINE_SEP = "|"

    __ANSWER = "ANSWER"  # user is expected to choose an answer
    __REPLY = ""  # basic type just reply
    __GIVE = "GIVE"

    __CONDITION_IF = "IF"
    __CONDITION_ELIF = "ELIF"
    __CONDITION_ELSE = "ELSE"

    def __init__(self, text, name, character_specific_data: "_CharacteSpecificData"):
        self._name = name  # for debugging purposes

        # possible behaviour trees chosen based on a statement that is tested based on memory and activity
        self.logic_paths = self._read_behavior(text, character_specific_data)

    def conversate(self, activity):
        # all separate paths all are tested consecutively
        for logic_path in self.logic_paths:
            behaviour_tree = logic_path.get_behaviour_tree(activity)
            # no statement in path satisfied
            if behaviour_tree is None:
                continue
            response_id = "0"
            while response_id != _Response.END_CONVERSATION_ID:
                response_id = behaviour_tree[response_id].trigger()

    def _read_behavior(self, text, character_specific_data):
        # remove the name line
        behaviour_tree = {}
        logic_paths = []
        previous_logic_statement = None
        for line in component_lines(text):
            line = self._substitute_data(line, character_specific_data)
            values = line.split(STATEMENT_SEP)
            if len(values) == 1:
                if previous_logic_statement is None:
                    previous_logic_statement = self._read_logic_statement(line, previous_logic_statement)
                    logic_paths.append(previous_logic_statement)
                else:
                    previous_logic_statement.set_behaviour_tree(behaviour_tree)
                    behaviour_tree = {}
                    new_logic_statement = self._read_logic_statement(line, previous_logic_statement)
                    if new_logic_statement.id == 0:
                        logic_paths.append(new_logic_statement)
                    else:
                        previous_logic_statement.set_next_statement(new_logic_statement)
                    previous_logic_statement = new_logic_statement
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

        # make sure to add the last behaviour tree
        if previous_logic_statement is not None:
            previous_logic_statement.set_behaviour_tree(behaviour_tree)
        # ensure that on empty statements a tree is added as well
        else:
            logic_paths.append(_LogicStatement(0, "", self._name))
            logic_paths[-1].set_behaviour_tree(behaviour_tree)
        return logic_paths

    def _read_logic_statement(
            self,
            line: str,
            prev_statement: Union["_LogicStatement", None]
    ) -> Union["_LogicStatement", None]:

        values = line.replace(":", "").split(" ", 1)
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

    def _substitute_data(self, line, character_specific_data: "_CharacteSpecificData") -> str:
        # TODO add tests for missing values of memory and inventory
        # substitute values in a line that are requested with { }
        substiute_values = re.findall("\{.+?\}", line)  # noqa
        for value in substiute_values:
            replace_value = "<NOT FOUND>"
            value_name = value.replace("}", "").split(".")[1]
            if INVENTORY_CONST in value:
                item_dict = character_specific_data.get_item(value_name)
                if item_dict is not None:
                    replace_value = str(next(iter(item_dict.values())))
            elif MEMORY_CONST in value:
                memory_value = character_specific_data.get_memory(value_name)
                if memory_value is not None:
                    replace_value = memory_value
            elif PLAYER_CONST in value:
                player_value = str(PlayerValues.ask_value(value_name))
                if player_value is not None:
                    replace_value = player_value
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.UNKNOWN_SUBSTITUTE_CONSTANT, debug_warning=True,
                                   constant=value.replace("{", "").split(".")[0])
                continue
            line = line.replace(value, replace_value)
        return line

    def _get_response_class(self, response_type) -> Union[Type["_Response"], None]:
        if response_type == self.__ANSWER:
            return _AnswerResponse
        if response_type == self.__REPLY:
            return _ReplyResponse
        # if response_type == self.__GIVE:
        #     return _GiveResponse
        lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_RESPONSE_TYPE, debug_warning=True, name=self._name,
                           type=response_type)
        return None


class _LogicStatement:
    # saves chains of elif logic pushing to the next statement if statement evaluates to false
    person: str
    id: int
    _statement_connector: Union[str, None]
    _statement_parts: List[List[str]]
    _next_statement: Union[None, "_LogicStatement"]
    _behaviour_tree: Union[None, Dict[int, "_Response"]]

    __ACTIVITY_NAME = "ACTIVITY"  # statements that are replaced with a boolean relating to activity

    __INVERSE = "NOT"
    __AND = "AND"
    __OR = "OR"
    __BIGGER_THEN = ">"
    __SMALLER_THEN = "<"
    __EQUALS = "=="

    __ALL_ALLOWED_CONSTANTS = {__ACTIVITY_NAME, __INVERSE, __BIGGER_THEN, __SMALLER_THEN, __EQUALS}
    __COMPARISSON_OPERATORS = {__EQUALS, __BIGGER_THEN, __SMALLER_THEN}

    def __init__(self, id_, statement, person):
        self.person = person
        self.id = id_
        self._statement_connector = None  # defaults to OR if no further info is provided
        self._statement_parts = self._read_statements(statement)

        self._next_statement = None  # next logic statment on evaluating false, default is no next statement
        self._behaviour_tree = None

    def _read_statements(self, statements: str):
        statments_values = statements.strip().split()
        statements_parts = []
        current_statement = []
        for value in statments_values:
            if value in (self.__AND, self.__OR):
                if self._statement_connector is None:
                    self._statement_connector = value
                elif self._statement_connector != value:
                    lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True,
                                       name=self.person, line=statements, extra="Cannot mix statement connectors")
                    break
                self.__add_statement(current_statement, statements_parts)
                current_statement = []
            else:
                if value.split('.')[0] not in self.__ALL_ALLOWED_CONSTANTS:
                    if not value.isdigit():
                        lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True,
                                           name=self.person, line=statements,
                                           extra="Invalid constant or integer provided")
                current_statement.append(value)
        self.__add_statement(current_statement, statements_parts)
        if self._statement_connector is None:
            self._statement_connector = self.__OR
        return statements_parts

    def __add_statement(self, statement_values, statements_parts):
        if len(statement_values) > 0:
            if len(set(statement_values) & self.__COMPARISSON_OPERATORS) > 0:
                if len(statement_values) != 3:
                    lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True,
                                       name=self.person, line=' '.join(statement_values),
                                       extra="Numerical comparissons must consist of value1 operator value2.")
                    return
            statements_parts.append(statement_values)

    def get_behaviour_tree(self, activity) -> Union[Dict[str, "_Response"], None]:
        if len(self._statement_parts) == 0:  # the else statemnt
            return self._behaviour_tree

        for statement in self._statement_parts:
            invert_statement = False
            statement_value = False
            # we have an integer comparisson
            if len(set(statement) & self.__COMPARISSON_OPERATORS) > 0:
                statement_value = self._do_integer_comparisson(statement)
            else:
                for statement_part in statement:
                    if statement_part == self.__INVERSE:
                        invert_statement = not invert_statement
                    elif statement_part.startswith(self.__ACTIVITY_NAME):
                        statement_value = statement_part.split(".")[1] == activity
            if invert_statement:
                statement_value = not statement_value
            if self._statement_connector == self.__OR:
                if statement_value:
                    return self._behaviour_tree
                elif self._next_statement is not None:
                    return self._next_statement.get_behaviour_tree(activity)
                else:
                    return None
            else:
                if not statement_value:
                    if self._next_statement is not None:
                        return self._next_statement.get_behaviour_tree(activity)
                    else:
                        return None
        if self._statement_connector == self.__AND:
            return self._behaviour_tree
        return None

    def _do_integer_comparisson(self, statement_values: List[str]):
        try:
            val1 = int(statement_values[0])
            val2 = int(statement_values[2])
        except ValueError:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_LOGIC, debug_warning=True, name=self.person,
                               line=' '.join(statement_values), extra="Values around operator are not integers")
            return False
        operator = statement_values[1]
        if operator == self.__SMALLER_THEN:
            return val1 < val2
        if operator == self.__BIGGER_THEN:
            return val1 > val2
        if operator == self.__EQUALS:
            return val1 == val2

    def set_behaviour_tree(self, behaviour_tree: Dict[int, "_Response"]):
        self._behaviour_tree = behaviour_tree

    def set_next_statement(self, statement: "_LogicStatement"):
        self._next_statement = statement


class _Response(ABC):
    END_CONVERSATION_ID = "-1"

    id: int
    next_ids: Union[List[str], None]
    text: str
    person: str

    def __init__(self, id_: int, talk_lines: List[str], responses: str, person: str):
        self.id = id_
        self.next_ids = self._disect_response_ids(responses)
        self.text = self._prepare_lines(talk_lines)
        self.person = person

    def _prepare_lines(self, lines: List[str]) -> str:
        return '\n'.join(lines)

    def _disect_response_ids(self, responses: str) -> Union[List[str], None]:
        if responses == "":
            return None
        numbers = responses.split()
        return numbers

    def trigger(self) -> str:
        continue_last = False if self.id == "0" else True
        if self.text != "":
            lazy_utility.message_person(self.text, self.person, continue_last=continue_last)
        return self.get_response_id()

    @abstractmethod
    def get_response_id(self) -> str:
        pass

    def __str__(self):
        return f"<Response object[id: {self.id}, next_ids: {self.next_ids}, text: {self.text}]>"

    def __repr__(self):
        return str(self)


class _ReplyResponse(_Response):
    # simply reply one or more options without further input

    def get_response_id(self) -> str:
        if self.next_ids is None:
            return self.END_CONVERSATION_ID  # end of conversation
        return random.choice(self.next_ids)

    def __str__(self):
        return f"<ReplyResponse object[id: {self.id}, next_ids: {self.next_ids}, text: {self.text}]>"


class _AnswerResponse(_Response):
    # expect an answer from the user
    def __init__(self, id_, lines, responses, person):
        self._total_answers = 0
        super().__init__(id_, lines, responses, person)

    def trigger(self) -> str:
        return self.get_response_id()

    def get_response_id(self) -> str:
        pass

    def __str__(self):
        return f"<AnswerResponse object[id: {self.id}, next_ids: {self.next_ids}, text: {self.text}]>"


class _GiveResponse(_Response):
    # TODO add tests
    # give an item to the player
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
            {str(index + 1): self.next_ids[index] for index in range(self._total_answers)})

    def _prepare_lines(self, lines: str) -> str:
        formatted_text = ""
        self._total_answers = len(lines)
        if self._total_answers <= 1:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning, debug_warning=True)
        for index, response in enumerate(lines):
            formatted_text += f"  [{index + 1}] {response}\n"
        return formatted_text[:-1]  # remove last newline

    def __str__(self):
        return f"<GiveResponse object[id: {self.id}, next_ids: {self.next_ids}, text: {self.text}]>"


class _CharacteSpecificData:

    def __init__(self, starting_data, name):
        self.name = name
        self._inventory = {}
        self._memory = {}
        self._read_character_data(starting_data)

    def get_item(self, name) -> Union[Dict[items.Item, int], None]:
        if name in self._inventory:
            return {items.ITEM_MAPPING[name]: int(self._inventory[name])}
        return None

    def get_memory(self, name) -> Union[str, None]:
        if name in self._memory:
            return self._memory[name]
        return None

    def _read_character_data(self, starting_data):
        active_user_dir = lazy_utility.active_user_dir(return_on_fail=None)
        if active_user_dir is None:
            return
        person_file_name = active_user_dir / lazy_constants.USER_PEOPLE_DIR / self.name
        # first time setup
        if not person_file_name.exists():
            self.__init_character_specific_data(person_file_name, starting_data)
        with open(person_file_name) as f:
            text = f.read()
        components = text.split(COMPONENT_SPLITTER)
        for component in components:
            if component == "":
                continue
            if component.startswith(INVENTORY_CONST):
                self._inventory = self._read_specific_data(component, is_item=True)
            elif component.startswith(MEMORY_CONST):
                self._memory = self._read_specific_data(component)
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_START_IDENTIFIER, debug_warning=True,
                                   name=component.split(";")[0])

    def __init_character_specific_data(self, person_file_name, starting_data):
        # function called if the file is not present. Will innitialize values based on character file
        inv_text_list = [f"{COMPONENT_SPLITTER}{INVENTORY_CONST}"]
        mem_text_list = [f"{COMPONENT_SPLITTER}{MEMORY_CONST}"]
        for line in component_lines(starting_data):
            values = line.strip().split(STATEMENT_SEP)
            if len(values) != 3:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_LINE, debug_warning=True,
                                   name=self.name, line=line)
                continue
            identifier, name, value = values
            if identifier == INVENTORY_CONST:
                inv_text_list.append(f"{name};{value}")
            elif identifier == MEMORY_CONST:
                mem_text_list.append(f"{name};{value}")
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_START_IDENTIFIER, debug_warning=True,
                                   identifier=identifier)

        with open(person_file_name, "w") as f:
            f.write('\n'.join(inv_text_list))
            f.write("\n")
            f.write('\n'.join(mem_text_list))

    def _read_specific_data(self, data, is_item=False):
        value_mapping = {}
        for line in component_lines(data):
            values = line.strip().split(STATEMENT_SEP)
            if len(values) != 2:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_PERSON_LINE, debug_warning=True,
                                   name=self.name, line=line)
                continue
            identifier, value = values
            if identifier in value_mapping:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.DOUBLE_DATA_ENTRY, debug_warning=True,
                                   name=self.name, identifier=identifier)
            if is_item:
                if identifier not in items.ITEM_MAPPING:
                    lazy_warnings.warn(lazy_warnings.LazyWarningMessages.INVALID_ITEM_NAME, debug_warning=True,
                                       name=identifier)
                    continue
                elif not value.isdigit():
                    lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_ITEM_QUANTITY, debug_warning=True)
                    continue
            value_mapping[identifier] = value
        return value_mapping


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
            if line.startswith(IGNORE_SYMBOL):
                continue
            values = line.strip().split(STATEMENT_SEP)
            if len(values) != 2:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INCOMPLETE_TIME_PATTERN_LINE, debug_warning=True,
                                   line=line, name=self.person)
                continue
            if values[1] == "":
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
            prev_time = time

            # since time goes from low to high
            for time in range(time, self.__HOURS_IN_DAY):
                time_dictionary[time] = activity
        return time_dictionary
