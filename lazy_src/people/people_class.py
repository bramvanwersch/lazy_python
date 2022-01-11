from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings


class Person:
    # person located at a location, can be used to talk to or sell stuff
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self._behaviour = self._load_person_interactions()

    def examine(self):
        lazy_utility.message(f"{self.name}: {self.description}")

    def talk(self):
        lazy_utility.message_person(f"I am not yet implemented :).", self.name)

    def _load_person_interactions(self):
        person_file = lazy_constants.PERSON_FOLDER / self.name
        if not person_file.exists():
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.MISSING_PERSON_FILE, debug_warning=True,
                               person=self.name)
            return None
        tree = BehaviourTree(person_file, self.name)
        return tree


class BehaviourTree:

    __SEP = ";"
    __COMMAND_MAPPING = {
        "END": 1
    }
    __BEHAVIOUR_NAME = "BEHAVIOUR"
    __STATS_NAME = "STATS"
    __TIME_PATTERNS_NAME = "TIME_PATTERNS"

    def __init__(self, person_file, name):
        self._read_person_file(person_file, name)

    def _read_person_file(self, file, name):
        with open(file) as f:
            text = f.read()
        components = text.split(">")
        for component in components:
            if component.startswith(self.__BEHAVIOUR_NAME):
                self._read_behavior(component)
            elif component.startswith(self.__STATS_NAME):
                self._read_stats(component)
            elif component.startswith(self.__TIME_PATTERNS_NAME):
                self._read_time_patterns(component)
            else:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning, debug_warning=True, person=name,
                                   name=component.split("\n")[0])

    def _read_behavior(self, text):
        pass

    def _read_stats(self, text):
        pass

    def _read_time_patterns(self, text):
        pass

    def _read_memory(self):
        # user dependant
        pass



