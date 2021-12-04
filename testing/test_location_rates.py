from sys import argv
from collections import defaultdict

from src.commands.explore import locations_definitions


def get_area_rates(requested_area):
    area = locations_definitions.AREAS[requested_area]
    area_header = f"# Information for area: {area.name} #"
    print("#" * len(area_header))
    print(area_header)
    print("#" * len(area_header))
    for location in area._locations.values():
        get_location_rates(location)


def get_location_rates(location):
    location_header = f"\t| Rates for {location.name}: |"
    print("\t" + "-" * len(location_header))
    print(location_header)
    print("\t" + "-" * len(location_header))
    for activity in location._activities:
        xp_dict, item_dict = get_activity_rates(activity)
        print_activity_data(xp_dict, item_dict, activity.name)


def print_activity_data(xp_dict, item_dict, activity_name):
    print(f"\tRates for activity: {activity_name}")
    print("\t\tXP rates (per hour):")
    for skill, xp in xp_dict.items():
        print(f"\t\t - {skill.name}: {round(xp, 5)} xp")
    print()
    print("\t\tItem rates (per hour):")
    for item, amnt in item_dict.items():
        print(f"\t\t - {item.name}: {round(amnt, 5)}")


def get_activity_rates(activity):
    base_succes_chance = activity._succes_chance
    rolls_per_hour = 3600 / activity.SIMULATE_EVERY
    total_table_weight = sum(activity._loot_table.values())

    total_item_dict = defaultdict(int)
    total_xp_dict = defaultdict(int)
    for loot, weight in activity._loot_table.items():
        # these are generally certain items that can be ignored in rates
        if loot.is_depletable():
            continue
        item_dict = defaultdict(int)
        xp_dict = defaultdict(int)
        roll_chance = weight / total_table_weight
        item_chance_per_roll = base_succes_chance * roll_chance
        total_times = rolls_per_hour * item_chance_per_roll
        loot.add_xp_and_items(xp_dict, item_dict)
        for skill, xp in xp_dict.items():
            total_xp_dict[skill] += xp * total_times

        for item, amnt in item_dict.items():
            total_item_dict[item] += amnt * total_times
    return total_xp_dict, total_item_dict


if __name__ == '__main__':
    req_area = argv[1]
    get_area_rates(req_area)