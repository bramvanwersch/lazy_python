from unittest import TestCase
import random

from lazy_src import lazy_constants
from lazy_src.commands import train
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
                         f"(....)> {lazy_constants.GREEN_COLOR}exploring: +300xp (0-15){lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered small_lake{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You discovered old_tree{lazy_constants.RESET_COLOR}\n"
                         "(lazy)> Started exploring green_woods...\n")

    def test_gather(self):
        # fishing and woodcutting are very much the same
        output, _ = testing_utility.capture_print(train.gather)
        self.assertEqual(output, "(lazy)> Nothing to check yet.\n"
                                 "(lazy)> Started gathering at home...\n")
        random.seed(1)
        # make sure the check is done properly
        output, _ = testing_utility.capture_print(train.gather)
        self.assertEqual(output,
                         "(lazy)> In total 3600s passed\n"
                         "(....)> The following things happened while you where away:\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}gathering: +4xp {lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 2 X old_bread{lazy_constants.RESET_COLOR}\n"
                         f"(....)> {lazy_constants.GREEN_COLOR}You found 4 X coin{lazy_constants.RESET_COLOR}\n"
                         "(lazy)> Started gathering at home...\n")
