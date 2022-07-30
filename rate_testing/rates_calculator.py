from typing import TYPE_CHECKING, Tuple, DefaultDict, Dict, List, Union
from collections import defaultdict

from lazy_src import areas
from lazy_src.areas import locations_classes

if TYPE_CHECKING:
    from lazy_src import items
    from lazy_src import skills


# TODO: cover exploring as well. Not that important


def main():
    xp_datas = []
    item_datas = []
    level_range = list(range(100))
    for area in areas.Areas.all_areas():
        xp_data, item_data = get_activity_rates(area, level_range)
        xp_datas.append(xp_data)
        item_datas.append(item_data)
    write_data(item_datas, level_range, "items_per_hour.tsv")
    write_data(xp_datas, level_range, "xp_per_hour.tsv")


def get_activity_rates(
    area: locations_classes.Area,
    levels: List[int]
) -> Tuple[Dict[Tuple[str, str, str], List[DefaultDict["skills.Skill", int]]],
           Dict[Tuple[str, str, str], List[DefaultDict["items.Item", int]]]]:
    all_xp_data = {}
    all_item_data = {}
    for location in area.locations.values():
        for activity in location.activities.values():
            xp_data, item_data = get_rate(activity, levels)
            all_xp_data[(area.name, location.name, activity.name)] = xp_data
            all_item_data[(area.name, location.name, activity.name)] = item_data
    return all_xp_data, all_item_data


def get_rate(
    activity: locations_classes.Activity,
    levels: List[int]
) -> Tuple[List[DefaultDict["skills.Skill", int]], List[DefaultDict["items.Item", int]]]:
    xp_level_list = []
    item_level_list = []
    for level in levels:
        base_succes_chance = activity.succes_chance
        level_succes_chance = activity.main_skill.get_additional_roll_chance_from_level(level)
        total_succes_chance = base_succes_chance + level_succes_chance
        replentishable_loot_table = {loot: weigth for loot, weigth in activity.loot_table.items()
                                     if not loot.is_depletable() and loot.required_level <= level}
        total_weight = sum(replentishable_loot_table.values())
        loot_chance_table = \
            {loot: (weigth / total_weight) * total_succes_chance for loot, weigth in replentishable_loot_table.items()}
        all_xp_data = defaultdict(int)
        all_item_data = defaultdict(int)
        rolls_per_hour = 3600 / locations_classes.Area.SIMULATE_EVERY
        for loot, chance in loot_chance_table.items():
            total_triggers = chance * rolls_per_hour
            for skill, xp in loot.xp_rewards.items():
                all_xp_data[skill] += xp * total_triggers
            for item, amnt in loot.item_rewards.items():
                all_item_data[item] = amnt * total_triggers

        xp_level_list.append(all_xp_data)
        item_level_list.append(all_item_data)
    return xp_level_list, item_level_list


def write_data(
    datas: List[Dict[Tuple[str, str, str], List[DefaultDict[Union["skills.Skill", "items.Item"], int]]]],
    levels: List[int],
    file_name: str
):
    lines = [["area", "location", "activity", "thing"] + list(map(str, levels))]
    size_per_column = [len(value) for value in lines[0]]
    for area_dct in datas:
        for (area_name, location_name, activity_name), level_dcts in area_dct.items():
            values = sorted(level_dcts[-1].keys(), key=lambda x: x.name)
            for value in values:
                line =\
                    [area_name, location_name, activity_name, value.name] + [f"{dct[value]:.3f}" for dct in level_dcts]
                size_per_column = \
                    [max(size_per_column[index], len(line[index])) for index in range(len(size_per_column))]
                lines.append(line)
    with open(file_name, "w") as f:
        for lst in lines:
            line = ""
            for index, value in enumerate(lst):
                line += value + " " * (size_per_column[index] - len(value) + 2)
            f.write(line + "\n")


if __name__ == '__main__':
    main()
