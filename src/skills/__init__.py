from src.skills._skills import *


class Skills:
    EXPLORING = Skill("exploring")
    GATHERING = Skill("gathering")
    WOODCUTTING = Skill("woodcutting")

    @classmethod
    def all_skills(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__")]
