from sys import argv

from lazy_src import areas
from lazy_src import skills


def simulate_area_rates(requested_area, start_level, total_rolls=1000):
    start_xp = skills.level_to_xp(start_level)
    area = areas.AREA_MAPPING[requested_area]
    area_header = f"# Information for area: {area.name} with {total_rolls} simulated rolls#"
    print("#" * len(area_header))
    print(area_header)
    print("#" * len(area_header))
    for location in area._locations.values():
        simulate_location_rates(location, start_xp, total_rolls)


def simulate_location_rates(location, start_xp, total_rolls):
    location_header = f"  | Rates for {location.name}: |"
    print("  " + "-" * len(location_header))
    print(location_header)
    print("  " + "-" * len(location_header))
    for activity in location.activities.values():
        xp_dict, item_dict = simulate_activity_rates(activity, start_xp, total_rolls)
        print_activity_data(xp_dict, item_dict, activity.name)


def print_activity_data(xp_dict, item_dict, activity_name):
    print(f"  Rates for activity: {activity_name}")
    print("    XP rates (per hour):")
    for skill_name, xp in xp_dict.items():
        if xp > 0:
            print(f"     - {skill_name}: {round(xp, 5)} xp")
    print()
    print("    Item rates (per hour):")
    for item_name, amnt in item_dict.items():
        print(f"     - {item_name}: {round(amnt, 5)}")
    print()


def simulate_activity_rates(activity, start_xp, total_rolls):
    wanted_passed_time = total_rolls * activity.SIMULATE_EVERY
    total_xp_dict, total_item_dict = activity.rate_simulate(wanted_passed_time, start_xp)
    total_hours_rolled = wanted_passed_time / 3600

    # remove all the starting xp
    for key in total_xp_dict:
        total_xp_dict[key] -= start_xp

    get_hour_rates(total_hours_rolled, total_xp_dict)
    get_hour_rates(total_hours_rolled, total_item_dict)

    return total_xp_dict, total_item_dict


def get_hour_rates(hours_passed, value_dict):
    for key in value_dict:
        value_dict[key] = round(value_dict[key] / hours_passed, 2)


if __name__ == '__main__':
    req_area = argv[1]
    try:
        starting_level = int(argv[2])
    except IndexError:
        starting_level = 0
    try:
        tot_rolls = int(argv[3])
    except IndexError:
        tot_rolls = 1000
    simulate_area_rates(req_area, starting_level, tot_rolls)
