from unittest import TestCase
import subprocess
import random

from src.areas import locations, green_woods_area_definitions
from src import skills
from src import constants
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
        unlocked_set = locations.get_unlocked_location_names()
        self.assertEqual({"home"}, unlocked_set)

    def test_area_exploration(self):
        random.seed(1)
        area = green_woods_area_definitions.green_woods
        xp_dict, location_dict = area.perform_activity_rolls("", skills.Skills.EXPLORING.name, 3600)
        self.assertEqual(xp_dict, {'Fishing': 0, 'exploring': 300, 'gathering': 0, 'woodcutting': 0})
        self.assertEqual(location_dict, {"small lake": 1, "old tree": 1})

    def test_area_train(self):
        random.seed(1)
        area = green_woods_area_definitions.green_woods
        xp_dict, item_dict = area.perform_activity_rolls(constants.STARTING_LOCATION, skills.Skills.GATHERING.name,
                                                         3600)
        self.assertEqual(xp_dict, {'exploring': 0, 'gathering': 4, 'woodcutting': 0, 'Fishing': 0})
        self.assertEqual(item_dict, {'old_bread': 2, 'coin': 4})
