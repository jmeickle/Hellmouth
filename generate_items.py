from item import *
from items import item_list

def generate_item(type):
    stats = item_list[type].copy()
    if stats.get("identical") is not None:
        stats = item_list[stats["identical"]].copy()

    itemclass = stats.pop("class")
    item = itemclass()

    item.name = type

    for stat, value in stats.items():
        setattr(item, stat, value)
    return item
