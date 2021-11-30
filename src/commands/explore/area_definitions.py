

class Area:

    def __init__(self, name, locations, xp_per_area, base_chance, lore=""):
        self.name = name
        self._locations = locations
        self._unlocked_locations = []
        self._xp_per_area = xp_per_area
        self._unlock_chance = base_chance
        self.lore = lore

    def unlock(self, passed_time):
        pass


class Location:
    def __init__(self, name, chance, xp, lore=""):
        self.name = name
        self.discovery_chance = chance
        self.lore = lore
        self._activities = []


# green woods
_green_wood_location = Area("green woods", [], 5, 0.1, "The starting are. The place one could call home.")


AREAS = {
    _green_wood_location.name: _green_wood_location
}
