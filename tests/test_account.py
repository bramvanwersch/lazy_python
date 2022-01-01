from unittest import TestCase

from src.commands import account
import testing_setup


class Test(TestCase):

    def setUp(self) -> None:
        testing_setup.setup_test_folder()

    def tearDown(self) -> None:
        testing_setup.remove_test_folder()

    def test_new(self):
        # inputs are not checked
        username = "test"
        password = "test"
        account.new(username, password, password)

    # def test__create_account(self):
    #     self.fail()
    #
    # def test_create_area_file(self):
    #     self.fail()
    #
    # def test_activate(self):
    #     self.fail()
    #
    # def test_info(self):
    #     self.fail()
    #
    # def test__show_general_information(self):
    #     self.fail()
    #
    # def test__show_levels(self):
    #     self.fail()
    #
    # def test__show_inventory(self):
    #     self.fail()
    #
    # def test_delete(self):
    #     self.fail()
    #
    # def test__get_username_password(self):
    #     self.fail()
    #
    # def test__confirm_password(self):
    #     self.fail()
