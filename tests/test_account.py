from unittest import TestCase

from src.commands import account
from src import constants
from src import utility


class Test(TestCase):

    def test_new(self):
        # inputs are not checked
        pass
        username = "test"
        password = "test"
        account.new(username, password, password)
        self.assertTrue(constants.K)

    def test__create_account(self):
        self.fail()

    def test_create_area_file(self):
        self.fail()

    def test_activate(self):
        self.fail()

    def test_info(self):
        self.fail()

    def test__show_general_information(self):
        self.fail()

    def test__show_levels(self):
        self.fail()

    def test__show_inventory(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test__get_username_password(self):
        self.fail()

    def test__confirm_password(self):
        self.fail()
