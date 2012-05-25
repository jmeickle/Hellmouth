from data import items

def generate_item(type):
    stats = items.item_list[type].copy()
    if stats.get("identical") is not None:
        stats = items.item_list[stats["identical"]].copy()

    itemclass = stats.pop("class")
    item = itemclass()

    item.name = type

    for stat, value in stats.items():
        setattr(item, stat, value)
    return item
