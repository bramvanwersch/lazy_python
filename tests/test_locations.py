from unittest import TestCase
import random

from lazy_src.areas import locations_classes, green_woods_area_definitions
from lazy_src import skills
from lazy_src import lazy_constants
import testing_setup


class TestLocation(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_get_unlocked_location_names(self):
        unlocked_set = locations_classes.get_unlocked_location_names()
        self.assertEqual({"home"}, unlocked_set)

    def test_area_exploration(self):
        random.seed(1)
        area = green_woods_area_definitions.green_woods
        xp_dict, location_dict = area.perform_activity_rolls("", skills.Skills.EXPLORING.name, 3600)
        self.assertEqual({"exploring": 300}, {key: value for key, value in xp_dict.items() if value != 0})
        self.assertEqual(location_dict, {"small_lake": 1, "old_tree": 1})

    def test_area_train(self):
        random.seed(1)
        area = green_woods_area_definitions.green_woods
        xp_dict, item_dict = area.perform_activity_rolls(lazy_constants.STARTING_LOCATION, skills.Skills.GATHERING.name,
                                                         3600)
        self.assertEqual({"gathering": 4}, {key: value for key, value in xp_dict.items() if value != 0})
        self.assertEqual(item_dict, {'old bread': 2, 'coin': 4})
