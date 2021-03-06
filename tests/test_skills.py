from unittest import TestCase

import testing_setup
from lazy_src import skills
from lazy_src import lazy_constants
from lazy_src import lazy_utility


class Test(TestCase):

    @classmethod
    def setUp(cls) -> None:
        testing_setup.setup_test_folder()
        testing_setup.create_test_account()

    @classmethod
    def tearDown(cls) -> None:
        testing_setup.remove_test_account()
        testing_setup.remove_test_folder()

    def test_add_xp(self):
        skills.add_xp({skills.Skills.WOODCUTTING.name: 100, skills.Skills.GATHERING.name: 500, "non-existing": 300})
        skills.add_xp({skills.Skills.WOODCUTTING.name: 100, skills.Skills.GATHERING.name: 500, "non-existing": 300})
        current_user_dir = lazy_utility.active_user_dir()
        level_dict = {}
        with open(current_user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            for line in f:
                key, value = line.strip().split(":")
                level_dict[key] = value
        self.assertEqual(level_dict["gathering"], "1000")
        self.assertEqual(level_dict["woodcutting"], "200")
        self.assertEqual(level_dict["non-existing"], "600")

    def test_set_xp(self):
        skills.set_xp({skills.Skills.WOODCUTTING.name: 100, skills.Skills.GATHERING.name: 500, "non-existing": 300})
        skills.set_xp({skills.Skills.WOODCUTTING.name: 10, skills.Skills.GATHERING.name: 50, "non-existing": 300})
        current_user_dir = lazy_utility.active_user_dir()
        level_dict = {}
        with open(current_user_dir / lazy_constants.USER_LEVEL_FILE_NAME) as f:
            for line in f:
                key, value = line.strip().split(":")
                level_dict[key] = value
        self.assertEqual(level_dict["gathering"], "50")
        self.assertEqual(level_dict["woodcutting"], "10")

    def test_get_xps(self):
        skills.add_xp({skills.Skills.WOODCUTTING.name: 100, skills.Skills.GATHERING.name: 500,
                       skills.Skills.FISHING.name: 300})
        xp_dict = skills.get_xps()
        self.assertEqual(xp_dict["gathering"], 500)
        self.assertEqual(xp_dict["fishing"], 300)

    def test_get_xp(self):
        skills.add_xp({skills.Skills.WOODCUTTING.name: 100, skills.Skills.GATHERING.name: 500,
                       skills.Skills.FISHING.name: 300})
        wc_xp = skills.get_xp(skills.Skills.WOODCUTTING.name)
        exploring_xp = skills.get_xp(skills.Skills.EXPLORING.name)
        self.assertEqual(wc_xp, 100)
        self.assertEqual(exploring_xp, 0)

    def test_get_levels(self):
        skills.add_xp({skills.Skills.WOODCUTTING.name: 1000, skills.Skills.GATHERING.name: 5,
                       skills.Skills.FISHING.name: 300})
        level_dict = skills.get_levels()
        self.assertEqual(level_dict["woodcutting"], 26)
        self.assertEqual(level_dict["fishing"], 15)

    def test_get_level(self):
        skills.add_xp({skills.Skills.WOODCUTTING.name: 1000, skills.Skills.GATHERING.name: 500,
                       skills.Skills.FISHING.name: 30})
        gather_level = skills.get_level(skills.Skills.GATHERING.name)
        fish_level = skills.get_level(skills.Skills.FISHING.name)
        self.assertEqual(gather_level, 19)
        self.assertEqual(fish_level, 2)

    def test_xp_to_level(self):
        level = skills.xp_to_level(10)
        self.assertEqual(level, 1)
        level = skills.xp_to_level(0)
        self.assertEqual(level, 0)
        level = skills.xp_to_level(999905)
        self.assertEqual(level, 100)
        level = skills.xp_to_level(999999905)
        self.assertEqual(level, 100)

    def test_level_to_xp(self):
        xp = skills.level_to_xp(100)
        self.assertEqual(xp, 999901)
        xp = skills.level_to_xp(0)
        self.assertEqual(xp, 0)
        xp = skills.level_to_xp(20)
        self.assertEqual(xp, 531)

    def test_xp_to_next_level(self):
        xp_left = skills.xp_to_next_level(99)
        self.assertEqual(xp_left, 10)
        xp_left = skills.xp_to_next_level(0)
        self.assertEqual(xp_left, 10)
        xp_left = skills.xp_to_next_level(1)
        self.assertEqual(xp_left, 9)
        xp_left = skills.xp_to_next_level(999901)
        self.assertEqual(xp_left, 0)

    def test_skill(self):
        fish_skill = skills.Skills.FISHING
        add_rol_chance = fish_skill.get_additional_roll_chance_from_xp(10)
        self.assertEqual(add_rol_chance, 0.005)
        add_rol_chance = fish_skill.get_additional_roll_chance_from_xp(500)
        self.assertEqual(add_rol_chance, 0.095)
