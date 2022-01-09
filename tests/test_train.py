from unittest import TestCase

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
        testing_utility.capture_print(train.explore)

    #
    # def test_gather(self):
    #     self.fail()
    #
    # def test_woodcut(self):
    #     self.fail()
    #
    # def test_fish(self):
    #     self.fail()
