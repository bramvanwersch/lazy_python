from typing import Dict

from lazy_src.items._items import ITEM_MAPPING, Item, WearableItem
from lazy_src import lazy_constants
from lazy_src import lazy_utility
from lazy_src import lazy_warnings


def get_equipment() -> "_Equipment":
    # will exit if no active user
    return _Equipment()


class _Equipment:

    def __init__(self):
        self._equipment = {}
        self._load()

    def _load(self):
        # exits if user not found
        user_dir = lazy_utility.active_user_dir()
        item_slots = WearableItem.all_equipment_slots()
        equiped_items = lazy_utility.get_values_from_file(user_dir / lazy_constants.USER_EQUIPMENT_FILE_NAME,
                                                          item_slots)
        self._equipment = {item_slots[index]: ITEM_MAPPING[name] for index, name in
                           enumerate(equiped_items) if name != ''}

    def get_equiped_items(self) -> Dict[str, Item]:
        return self._equipment

    def equip_items(
        self,
        equipment: Dict[str, Item]
    ):
        # will exit on fail
        user_dir = lazy_utility.active_user_dir()
        possible_slots = set(WearableItem.all_equipment_slots())
        accepted_slots = {}
        for slot, item in equipment.items():
            if slot not in possible_slots:
                lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_EQUIPMENT_SLOT, name=slot)
                continue
            accepted_slots[slot] = item
        lazy_utility.set_values_in_file(user_dir / lazy_constants.USER_EQUIPMENT_FILE_NAME, list(accepted_slots.keys()),
                                        [value.name for value in accepted_slots.values()])
        self._load()

    def get_equipment_at_slot(
        self,
        slot: str
    ) -> Item:
        try:
            return self._equipment[slot]
        except KeyError:
            lazy_warnings.warn(lazy_warnings.DevelopLazyWarning.INVALID_EQUIPMENT_SLOT, name=slot)
            raise SystemExit("Invalid slot selected")
