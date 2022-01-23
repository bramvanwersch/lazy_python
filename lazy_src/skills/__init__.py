from lazy_src.skills._skills import *


class Skills:
    EXPLORING = Skill("exploring")

    # gathering skills
    GATHERING = Skill("gathering")
    WOODCUTTING = Skill("woodcutting")
    FISHING = Skill("fishing")
    MINING = Skill("mining")
    STEALING = Skill("stealing")
    FARMING = Skill("farming")
    ARCHEOLOGY = Skill("archeology")
    HUNTING = Skill("hunting")

    # combat TO BE IMPLEMENTED
    RANGING = Skill("ranging")
    FIGHTING = Skill("fighting")
    SPELLCASTING = Skill("spellcasting")

    # buffing skill TO BE IMPLEMENTED
    WORSHIPPING = Skill("worshipping")

    # creating skills TO BE IMPLEMENTED
    # for ranging
    LEATHERWORKING = Skill("leatherworking")
    FLECTHING = Skill("fletching")

    # for mage
    WEAVING = Skill("weaving")

    # for melee
    ARMOR_SMITHING = Skill("armor_smithing")
    WEAPON_SMITHING = Skill("weapon_smithing")

    # general
    BREWING = Skill("brewing")
    BUILDING = Skill("building")
    COOKING = Skill("cooking")
    WRITING = Skill("writing")

    @classmethod
    def all_skills(cls):
        return [varvalue for varname, varvalue in vars(cls).items() if not varname.startswith("__") and
                varname != "all_skills"]
