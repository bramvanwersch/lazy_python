from src.skills._skills import *


class Skills:
    EXPLORING = Skill("exploring")
    GATHERING = Skill("gathering")
    WOODCUTTING = Skill("woodcutting")
    FISHING = Skill("Fishing")

    @classmethod
    def all_skills(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname != "all_skills"]
