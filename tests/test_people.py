from unittest import TestCase

from lazy_src.people import people
from lazy_src import lazy_constants
import testing_utility
import testing_setup


class TestPerson(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_folder()

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

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_folder()

    def test_conversate(self):
        self.fail()

    def test__read_behavior(self):
        self.fail()

    def test__read_logic_statement(self):
        self.fail()

    def test__get_response_class(self):
        self.fail()


class TestLogicStatement(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_folder()

    def test_read_statement(self):
        # simple instantiation
        statement = people._LogicStatement(1, "ACTIVITY.working", "test")
        self.assertEqual(statement._statement_connector, "OR")
        self.assertEqual(statement._statement_parts, [["ACTIVITY.working"]])

        # not statement
        statement = people._LogicStatement(1, "NOT ACTIVITY.working", "test")
        self.assertEqual(statement._statement_connector, "OR")
        self.assertEqual(statement._statement_parts, [["NOT", "ACTIVITY.working"]])

        # use integer comparissons
        statement = people._LogicStatement(1, "PLAYER.money > 50", "test")
        self.assertEqual(statement._statement_connector, "OR")
        # player money is set to 100 for testing
        self.assertEqual(statement._statement_parts, [["100", ">", "50"]])

        # and statement
        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND NOT ACTIVITY.sleeping", "test")
        self.assertEqual(statement._statement_connector, "AND")
        self.assertEqual(statement._statement_parts, [["NOT", "ACTIVITY.working"], ["NOT", "ACTIVITY.sleeping"]])

        # or statement
        statement = people._LogicStatement(1, "NOT ACTIVITY.testing OR NOT ACTIVITY.sleeping", "test")
        self.assertEqual(statement._statement_connector, "OR")
        self.assertEqual(statement._statement_parts, [["NOT", "ACTIVITY.testing"], ["NOT", "ACTIVITY.sleeping"]])

    def test_fail_read_statement(self):
        # testing if incorrect logic is catched

        # wrong keyword
        output, statement = testing_utility.capture_print(people._LogicStatement, 1, "ACTIVIY.working", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line 'ACTIVIY.working'. Invalid constant or integer provided"
                                 f"{lazy_constants.RESET_COLOR}\n")

        # mixing AND and OR
        output, statement = testing_utility.capture_print(
            people._LogicStatement, 1, "ACTIVITY.working AND ACTIVITY.testing OR NOT ACTIVITY.testing", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line 'ACTIVITY.working AND ACTIVITY.testing OR NOT "
                                 f"ACTIVITY.testing'. Cannot mix statement connectors{lazy_constants.RESET_COLOR}\n")

        # wrong integer comparisson
        output, statement = testing_utility.capture_print(
            people._LogicStatement, 1, "PLAYER.money > test", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line 'PLAYER.money > test'. Invalid constant or integer provided"
                                 f"{lazy_constants.RESET_COLOR}\n")

        output, statement = testing_utility.capture_print(
            people._LogicStatement, 1, "PLAYER.money >", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line '100 >'. Numerical comparissons must consist of value1 "
                                 f"operator value2.{lazy_constants.RESET_COLOR}\n")

    def test_get_behaviour_tree(self):
        # simple test succes
        statement = people._LogicStatement(1, "ACTIVITY.working", "test")
        response = people._ReplyResponse(1, ["hey"], "", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("working")
        self.assertEqual(behaviour_tree, {1: response})

        # make sure nothing is returned
        statement = people._LogicStatement(1, "ACTIVITY.working", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, None)

        # make sure simple inverse works
        statement = people._LogicStatement(1, "NOT ACTIVITY.working", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response})

        # make sure nothing is returned
        statement = people._LogicStatement(1, "NOT ACTIVITY.working", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("working")
        self.assertEqual(behaviour_tree, None)

        # use of OR
        statement = people._LogicStatement(1, "NOT ACTIVITY.working OR ACTIVITY.walking", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response})

        # also make sure nothing is returned
        statement = people._LogicStatement(1, "NOT ACTIVITY.working OR ACTIVITY.walking", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("working")
        self.assertEqual(behaviour_tree, None)

        # use of AND
        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND NOT ACTIVITY.walking", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("cooking")
        self.assertEqual(behaviour_tree, {1: response})

        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND NOT ACTIVITY.walking", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, None)

        # check with integer checks
        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND PLAYER.money > 50", "test")  # testing value 100
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response})

        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND PLAYER.money < 50", "test")  # testing value 100
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, None)

    def test_get_behaviour_tree_chained(self):
        # test if works with elif/ else statements
        response1 = people._ReplyResponse(1, ["hey1"], "", "test")
        response2 = people._ReplyResponse(1, ["hey2"], "", "tost")
        response3 = people._ReplyResponse(1, ["hey3"], "", "tast")

        # check with else
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND PLAYER.money < 50", "test")  # is false
        statement1.set_behaviour_tree({1: response1})
        statement2 = people._LogicStatement(2, "", "tost")
        statement2.set_behaviour_tree({1: response2})
        statement1.set_next_statement(statement2)
        behaviour_tree = statement1.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response2})

        # check with elif on true
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND PLAYER.money < 50", "test")
        statement1.set_behaviour_tree({1: response1})
        statement2 = people._LogicStatement(2, "ACTIVITY.walking", "tost")
        statement2.set_behaviour_tree({1: response2})
        statement1.set_next_statement(statement2)
        statement3 = people._LogicStatement(3, "", "tost")
        statement3.set_behaviour_tree({1: response3})
        statement2.set_next_statement(statement3)
        behaviour_tree = statement1.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response2})

        # check with elif on false
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND PLAYER.money < 50", "test")
        statement1.set_behaviour_tree({1: response1})
        statement2 = people._LogicStatement(2, "ACTIVITY.walking", "tost")
        statement2.set_behaviour_tree({1: response2})
        statement1.set_next_statement(statement2)
        statement3 = people._LogicStatement(3, "", "tost")
        statement3.set_behaviour_tree({1: response3})
        statement2.set_next_statement(statement3)
        behaviour_tree = statement1.get_behaviour_tree("cooking")
        self.assertEqual(behaviour_tree, {1: response3})


class TestTimeActivities(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_folder()

    def test_get_current_activity(self):
        self.fail()

    def test__read_pattern_lines(self):
        self.fail()
