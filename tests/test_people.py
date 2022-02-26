from unittest import TestCase

from lazy_src.people import people
from lazy_src.items import ITEM_MAPPING
from lazy_src import lazy_constants, lazy_utility
import testing_utility
import testing_setup


class TestResponseTree(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_conversate(self):

        empty_character_data = people._CharacteSpecificData("", "test")

        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)
        output, _ = testing_utility.capture_print(tree.conversate, "")
        self.assertEqual(
            output,
            f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: Sup test{lazy_constants.RESET_COLOR}\n"
            f"(....)> {lazy_constants.CONVERSATION_COLOR}test sais: Sup Son{lazy_constants.RESET_COLOR}\n")

        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "#ignore this\n"
            "IF ACTIVITY.sleeping:\n"
            "0;test is sleeping I better not talk to her;;player;\n"
            "ELSE:\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)
        output, _ = testing_utility.capture_print(tree.conversate, "sleeping")
        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: test is sleeping I better not "
                         f"talk to her{lazy_constants.RESET_COLOR}\n")
        output, _ = testing_utility.capture_print(tree.conversate, "")
        self.assertEqual(
            output,
            f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: Sup test{lazy_constants.RESET_COLOR}\n"
            f"(....)> {lazy_constants.CONVERSATION_COLOR}test sais: Sup Son{lazy_constants.RESET_COLOR}\n")

        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "IF ACTIVITY.sleeping:\n"
            "0;test is sleeping I better not talk to her;;player;\n"
            "ELIF ACTIVITY.cooking:\n"
            "0;cooking coenkies!!;;;\n"
            "ELSE:\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)

        output, _ = testing_utility.capture_print(tree.conversate, "sleeping")
        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: test is sleeping I better not "
                         f"talk to her{lazy_constants.RESET_COLOR}\n")

        output, _ = testing_utility.capture_print(tree.conversate, "cooking")
        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.CONVERSATION_COLOR}test sais: cooking coenkies!!"
                         f"{lazy_constants.RESET_COLOR}\n")

        output, _ = testing_utility.capture_print(tree.conversate, "anything else")
        self.assertEqual(
            output,
            f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: Sup test{lazy_constants.RESET_COLOR}\n"
            f"(....)> {lazy_constants.CONVERSATION_COLOR}test sais: Sup Son{lazy_constants.RESET_COLOR}\n")

    def test_read_behavior(self):
        # test no logic statements

        empty_character_data = people._CharacteSpecificData("", "test")

        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)
        all_statements = []
        all_behaviour_trees = []
        for logic_path in tree.logic_paths:
            while logic_path is not None:
                all_statements.append(logic_path._statement_parts)
                all_behaviour_trees.append(str(logic_path._behaviour_tree))
                logic_path = logic_path._next_statement
        self.assertEqual(all_statements, [[]])
        self.assertEqual(all_behaviour_trees,
                         ["{'0': <ReplyResponse object[id: 0, next_ids: ['1'], text: Sup test]>, '1': "
                          '<ReplyResponse object[id: 1, next_ids: None, text: Sup Son]>}'])

        # test simple if else statement
        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "IF ACTIVITY.sleeping:\n"
            "0;test is sleeping I better not talk to her;;player;\n"
            "ELSE:\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)
        all_statements = []
        all_behaviour_trees = []
        for logic_path in tree.logic_paths:
            while logic_path is not None:
                all_statements.append(logic_path._statement_parts)
                all_behaviour_trees.append(str(logic_path._behaviour_tree))
                logic_path = logic_path._next_statement
        self.assertEqual(all_statements, [[['ACTIVITY.sleeping']], []])
        self.assertEqual(all_behaviour_trees,
                         ["{'0': <ReplyResponse object[id: 0, next_ids: None, text: test is sleeping I better "
                          "not talk to her]>}",
                          "{'0': <ReplyResponse object[id: 0, next_ids: ['1'], text: Sup test]>, '1': "
                          "<ReplyResponse object[id: 1, next_ids: None, text: Sup Son]>}"])

        # test simple if elif else statement
        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "IF ACTIVITY.sleeping:\n"
            "0;test is sleeping I better not talk to her;;player;\n"
            "ELIF {PLAYER.money} > 50:\n"
            "0;Me rich baby!!;;player;\n"
            "ELSE:\n"
            "0;Sup test;1;player;\n"
            "1;Sup Son;;;\n",
            "test", empty_character_data)
        all_statements = []
        all_behaviour_trees = []
        for logic_path in tree.logic_paths:
            while logic_path is not None:
                all_statements.append(logic_path._statement_parts)
                all_behaviour_trees.append(str(logic_path._behaviour_tree))
                logic_path = logic_path._next_statement
        self.assertEqual(all_statements, [[['ACTIVITY.sleeping']], [['100', '>', '50']], []])
        self.assertEqual(all_behaviour_trees,
                         ["{'0': <ReplyResponse object[id: 0, next_ids: None, text: test is sleeping I "
                          'better not talk to her]>}',
                          "{'0': <ReplyResponse object[id: 0, next_ids: None, text: Me rich baby!!]>}",
                          "{'0': <ReplyResponse object[id: 0, next_ids: ['1'], text: Sup test]>, '1': "
                          '<ReplyResponse object[id: 1, next_ids: None, text: Sup Son]>}'])

    def test_read_behavior_fail(self):
        # invalid file line
        empty_character_data = people._CharacteSpecificData("", "test")

        output, tree = testing_utility.capture_print(people._ResponseTree, ">>>BEHAVIOUR\n1;col;ops;", "test",
                                                     empty_character_data)
        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.WARNING_COLOR}Person test encountered an invalid line: 1;col;ops;"
                         f".{lazy_constants.RESET_COLOR}\n")

        # empty elif statement
        output, tree = testing_utility.capture_print(people._ResponseTree, ">>>BEHAVIOUR\nELIF:\n1;col;ops;;", "test",
                                                     empty_character_data)
        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains invalid logic "
                         f"for line 'ELIF:'. no statement for elif{lazy_constants.RESET_COLOR}\n")

    def test_read_behaviour_inv_memory_substitutions(self):
        character_data = people._CharacteSpecificData(">>>START\n"
                                                      "INVENTORY;coin;5\n"
                                                      "MEMORY;test;this is a testing message", "test")

        tree = people._ResponseTree(
            ">>>BEHAVIOUR\n"
            "0;Sup test. I have {PLAYER.money} coins. WBU?;1;player;\n"
            "1;Sup Bro. I have {INVENTORY.coin} money. I like to say {MEMORY.test};;;\n",
            "test", character_data)

        output, _ = testing_utility.capture_print(tree.conversate, "")

        self.assertEqual(output,
                         f"(lazy)> {lazy_constants.CONVERSATION_COLOR}player sais: Sup test. I have 100 coins."
                         f" WBU?{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.CONVERSATION_COLOR}test sais: Sup Bro. I have 5 money. I like "
                         f"to say this is a testing message{lazy_constants.RESET_COLOR}\n")

    def test_read_behaviour_inv_memory_substitutions_fail(self):
        character_data = people._CharacteSpecificData(">>>START\n"
                                                      "INVENTORY;coin;5\n"
                                                      "MEMORY;test;this is a testing message", "test")

        output, tree = testing_utility.capture_print(
            people._ResponseTree,
            ">>>BEHAVIOUR\n"
            "0;Sup test. I have {KLAYERONI.money} coins. WBU?;1;player;\n"
            "1;Sup Bro. I have {INVENTORY.coin} money. I like to say {MEMORY.test};;;\n",
            "test", character_data)

        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Can not substitute with constant 'KLAYERONI'."
                                 f"{lazy_constants.RESET_COLOR}\n")


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
        statement = people._LogicStatement(1, "100 > 50", "test")
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
            people._LogicStatement, 1, "100 > test", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line '100 > test'. Invalid constant or integer provided"
                                 f"{lazy_constants.RESET_COLOR}\n")

        output, statement = testing_utility.capture_print(
            people._LogicStatement, 1, "100 >", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person file for person 'test' contains "
                                 f"invalid logic for line '100 >'. Numerical comparissons must consist of value1 "
                                 f"operator value2.{lazy_constants.RESET_COLOR}\n")

    def test_get_behaviour_tree(self):
        # simple test succes
        statement = people._LogicStatement(1, "ACTIVITY.working", "test")
        response = people._ReplyResponse(1, ["hey"], "", "test", people._CharacteSpecificData("", "test"))
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
        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND 100 > 50", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response})

        statement = people._LogicStatement(1, "NOT ACTIVITY.working AND 100 < 50", "test")
        statement.set_behaviour_tree({1: response})
        behaviour_tree = statement.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, None)

    def test_get_behaviour_tree_chained(self):
        # test if works with elif/ else statements
        response1 = people._ReplyResponse(1, ["hey1"], "", "test", people._CharacteSpecificData("", "test"))
        response2 = people._ReplyResponse(1, ["hey2"], "", "tost", people._CharacteSpecificData("", "tost"))
        response3 = people._ReplyResponse(1, ["hey3"], "", "tast", people._CharacteSpecificData("", "tast"))

        # check with else
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND 100 < 50", "test")  # is false
        statement1.set_behaviour_tree({1: response1})
        statement2 = people._LogicStatement(2, "", "tost")
        statement2.set_behaviour_tree({1: response2})
        statement1.set_next_statement(statement2)
        behaviour_tree = statement1.get_behaviour_tree("walking")
        self.assertEqual(behaviour_tree, {1: response2})

        # check with elif on true
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND 100 < 50", "test")
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
        statement1 = people._LogicStatement(1, "NOT ACTIVITY.working AND 100 < 50", "test")
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

    def test_read_pattern_lines(self):
        # simple version
        time_activities = people._TimeActivities(">>>TIME_PATTERNS\n0;sleeping\n7;cooking\n10;cleaning", "test")
        self.assertEqual(time_activities.get_current_activity(0), "sleeping")
        self.assertEqual(time_activities.get_current_activity(8), "cooking")
        self.assertEqual(time_activities.get_current_activity(23), "cleaning")

        # certain values unfilled
        time_activities = people._TimeActivities(">>>TIME_PATTERNS\n10;cleaning", "test")
        self.assertEqual(time_activities.get_current_activity(0), None)
        self.assertEqual(time_activities.get_current_activity(8), None)
        self.assertEqual(time_activities.get_current_activity(23), "cleaning")

    def test_read_pattern_lines_fail1(self):
        # simple version
        output, _ = testing_utility.capture_print(people._TimeActivities, ">>>TIME_PATTERNS\n0", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid time_pattern line '0' for person "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_read_pattern_lines_fail2(self):
        output, _ = testing_utility.capture_print(people._TimeActivities, ">>>TIME_PATTERNS\n0;", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid time_pattern line '0;' for person "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_read_pattern_lines_fail3(self):
        output, _ = testing_utility.capture_print(people._TimeActivities, ">>>TIME_PATTERNS\nga;cooling", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid time 'ga' for person "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_read_pattern_lines_fail4(self):
        output, _ = testing_utility.capture_print(people._TimeActivities, ">>>TIME_PATTERNS\n24;cooling", "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid time '24' for person "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")

    def test_read_pattern_lines_fail5(self):
        output, _ = testing_utility.capture_print(people._TimeActivities, ">>>TIME_PATTERNS\n2;cooling\n2;cooking",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Invalid time '2' for person "
                                 f"'test'.{lazy_constants.RESET_COLOR}\n")


class TestCharacteSpecificData(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_read_character_data(self):
        character_data = people._CharacteSpecificData(">>>START\n"
                                                      "# general_separator, item_name, quantity\n"
                                                      "INVENTORY;coin;5\n"
                                                      "MEMORY;test;this is a testing message", "test")
        self.assertEqual(character_data._memory, {'test': 'this is a testing message'})
        self.assertEqual(character_data._inventory, {"coin": 5})

    def test_read_character_data_fail1(self):
        output, _ = testing_utility.capture_print(people._CharacteSpecificData,
                                                  ">>>START\n"
                                                  "# general_separator, item_name, quantity\n"
                                                  "INVORY;coin;5\n"
                                                  "MEMORY;test;this is a testing message",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No identifier with name 'INVORY' allowed as "
                                 f"start identifier.{lazy_constants.RESET_COLOR}\n")

    def test_read_character_data_fail2(self):
        output, _ = testing_utility.capture_print(people._CharacteSpecificData,
                                                  ">>>START\n"
                                                  "# general_separator, item_name, quantity\n"
                                                  "INVENTORY;coin\n"
                                                  "MEMORY;test;this is a testing message",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Person test encountered an invalid line: "
                                 f"INVENTORY;coin.{lazy_constants.RESET_COLOR}\n")

    def test_read_character_data_fail3(self):
        output, _ = testing_utility.capture_print(people._CharacteSpecificData,
                                                  ">>>START\n"
                                                  "# general_separator, item_name, quantity\n"
                                                  "INVENTORY;coin;test\n"
                                                  "MEMORY;test;this is a testing message",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Expected an integer as item quantitiy"
                                 f".{lazy_constants.RESET_COLOR}\n")

    def test_read_character_data_fail4(self):
        output, _ = testing_utility.capture_print(people._CharacteSpecificData,
                                                  ">>>START\n"
                                                  "# general_separator, item_name, quantity\n"
                                                  "INVENTORY;cron;1\n"
                                                  "MEMORY;test;this is a testing message",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}No item with name 'cron' exists"
                                 f".{lazy_constants.RESET_COLOR}\n")

    def test_read_character_data_fail5(self):
        output, _ = testing_utility.capture_print(people._CharacteSpecificData,
                                                  ">>>START\n"
                                                  "# general_separator, item_name, quantity\n"
                                                  "INVENTORY;coin;1\n"
                                                  "INVENTORY;coin;60\n"
                                                  "MEMORY;test;this is a testing message",
                                                  "test")
        self.assertEqual(output, f"(lazy)> {lazy_constants.WARNING_COLOR}Double data entry with identifier 'coin' for "
                                 f"person test.{lazy_constants.RESET_COLOR}\n")

    def test_remove_items(self):
        character_data = people._CharacteSpecificData(">>>START\n"
                                                      "# general_separator, item_name, quantity\n"
                                                      "INVENTORY;coin;5\n"
                                                      "MEMORY;test;this is a testing message", "test")
        removed_items = character_data.remove_items({ITEM_MAPPING["coin"]: 6})
        self.assertEqual(removed_items, {ITEM_MAPPING["coin"]: 5})
        active_user_dir = lazy_utility.active_user_dir("test")
        person_file = active_user_dir / lazy_constants.USER_PEOPLE_DIR / "test"
        with open(person_file) as f:
            text = f.read()
        self.assertEqual(text, ">>>INVENTORY\ncoin;0\n>>>MEMORY\ntest;this is a testing message")

    def test_add_items(self):
        character_data = people._CharacteSpecificData(">>>START\n"
                                                      "# general_separator, item_name, quantity\n"
                                                      "INVENTORY;coin;15\n"
                                                      "MEMORY;test;this is a testing message", "test")
        character_data.add_items({ITEM_MAPPING["coin"]: 6})
        self.assertEqual(character_data._inventory["coin"], 21)
        active_user_dir = lazy_utility.active_user_dir("test")
        person_file = active_user_dir / lazy_constants.USER_PEOPLE_DIR / "test"
        with open(person_file) as f:
            text = f.read()
        self.assertEqual(text, ">>>INVENTORY\ncoin;21\n>>>MEMORY\ntest;this is a testing message")
