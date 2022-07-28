from unittest import TestCase
import random

from lazy_src import lazy_constants
from lazy_src.commands import train
from lazy_src import skills
from lazy_src import lazy_utility
from lazy_src.commands import general_commands
import testing_setup
import testing_utility


class Test(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_explore(self):
        output, _ = testing_utility.capture_print(train.explore)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n"
                                 "(lazy)> Started exploring green_woods...\n")
        random.seed(1)
        # make sure the check is done properly
        output, _ = testing_utility.capture_print(train.explore)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +330xp (0-15){lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_quarry{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_tree{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered small_lake{lazy_constants.RESET_COLOR}\n"
                         
                         "(lazy)> Started exploring green_woods...\n")

    def test_set_training_skill(self):
        output, _ = testing_utility.capture_print(train._set_training_skill, skills.Skills.GATHERING)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n"
                                 "(lazy)> Started gathering at home...\n")
        random.seed(1)
        # make sure the check is done properly
        output, _ = testing_utility.capture_print(train.gather)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n"
                         "(lazy)> Started gathering at home...\n")

    def test_set_training_skill_not_at_location(self):
        output, _ = testing_utility.capture_print(train._set_training_skill, skills.Skills.FISHING)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n"
                                 f"(lazy)> {lazy_constants.WARNING_COLOR}Can not train fishing at this location. Choose"
                                 f" one of the following: gathering.{lazy_constants.RESET_COLOR}\n")

    def test_set_training_skill_to_low_level(self):
        lazy_utility.set_values_in_file(lazy_utility.active_user_area_dir() / "green_woods",
                                        [lazy_constants.USERFILE_AREA_UNLOCKED_LOCATIONS],
                                        [','.join(["old_quarry"])])
        general_commands.move_location("green_woods", "old_quarry")
        output, _ = testing_utility.capture_print(train._set_training_skill, skills.Skills.GATHERING)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n"
                                 f"(lazy)> {lazy_constants.WARNING_COLOR}Level 5 gathering is required for activity"
                                 f" gathering{lazy_constants.RESET_COLOR}\n")
