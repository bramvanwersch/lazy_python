from unittest import TestCase

from lazy_src.people import people
from lazy_src import lazy_constants


class TestPerson(TestCase):
    def test_examine(self):
        self.fail()

    def test_talk(self):
        self.fail()

    def test__read_person_file(self):
        self.fail()

    def test__read_stats(self):
        self.fail()

    def test__read_memory(self):
        self.fail()


class TestResponseTree(TestCase):
    def test_conversate(self):
        self.fail()

    def test__read_behavior(self):
        self.fail()

    def test__read_logic_statement(self):
        self.fail()

    def test__get_response_class(self):
        self.fail()


class TestLogicStatement(TestCase):
    def test_read_statement(self):
        # simple instantiation
        statement = people._LogicStatement(1, "NOT ACTIVIES.working", "test")
        self.assertEqual(statement._statement_connector, "OR")
        self.assertEqual(statement._statement_parts, [["NOT ACTIVIES.working"]])

        # more difficult
        statement = people._LogicStatement(1, "NOT ACTIVIES.working AND MEMORY.time", "test")
        self.assertEqual(statement._statement_connector, "OR")
        self.assertEqual(statement._statement_parts, [["NOT ACTIVIES.working"]])

    def test_get_behaviour_tree(self):
        self.fail()

    def test_set_behaviour_tree(self):
        self.fail()

    def test_set_next_statement(self):
        self.fail()


class TestTimeActivities(TestCase):
    def test_get_current_activity(self):
        self.fail()

    def test__read_pattern_lines(self):
        self.fail()
