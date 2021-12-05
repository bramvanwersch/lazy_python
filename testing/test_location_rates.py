from sys import argv
from collections import defaultdict

from src.commands.explore import locations_definitions
from src import skills


def get_area_rates(requested_area, start_level):
    start_xp = skills.level_to_xp(start_level)
    area = locations_definitions.AREAS[requested_area]
    area_header = f"# Information for area: {area.name} #"
    print("#" * len(area_header))
    print(area_header)
    print("#" * len(area_header))
    for location in area._locations.values():
        get_location_rates(location, start_xp)


def get_location_rates(location, start_xp):
    location_header = f"  | Rates for {location.name}: |"
    print("  " + "-" * len(location_header))
    print(location_header)
    print("  " + "-" * len(location_header))
    for activity in location._activities:
        xp_dict, item_dict = get_activity_rates(activity, start_xp)
        print_activity_data(xp_dict, item_dict, activity.name)


def print_activity_data(xp_dict, item_dict, activity_name):
    print(f"  Rates for activity: {activity_name}")
    print("    XP rates (per hour):")
    for skill, xp in xp_dict.items():
        print(f"     - {skill.name}: {round(xp, 5)} xp")
    print()
    print("    Item rates (per hour):")
    for item, amnt in item_dict.items():
        print(f"     - {item.name}: {round(amnt, 5)}")
    print()


def get_activity_rates(activity, start_xp):
    base_succes_chance = activity._succes_chance
    rolls_per_hour = 3600 / activity.SIMULATE_EVERY
    total_table_weight = sum(activity._loot_table.values())

    total_item_dict = defaultdict(int)
    total_xp_dict = defaultdict(int)

    # track xp to factor in level bonus
    xp_gained_dict = defaultdict(lambda: start_xp)
    activity_skill = activity._main_skill

    for loot, weight in activity._loot_table.items():
        # these are generally certain items that can be ignored in rates
        if loot.is_depletable():
            continue

        additional_roll_chance = activity_skill.get_additional_roll_chance(xp_gained_dict[activity_skill])
        item_dict = defaultdict(int)
        xp_dict = defaultdict(int)
        roll_chance = weight / total_table_weight
        item_chance_per_roll = (base_succes_chance + additional_roll_chance) * roll_chance
        total_times = rolls_per_hour * item_chance_per_roll
        loot.add_xp_and_items(xp_dict, item_dict)
        for skill, xp in xp_dict.items():
            total_xp_dict[skill] += xp * total_times

        for item, amnt in item_dict.items():
            total_item_dict[item] += amnt * total_times
    return total_xp_dict, total_item_dict


if __name__ == '__main__':
    req_area = argv[1]
    try:
        starting_level = int(argv[2])
    except IndexError:
        starting_level = 0
    get_area_rates(req_area, starting_level)
