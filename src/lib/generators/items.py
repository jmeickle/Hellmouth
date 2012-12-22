# TODO: Better way of importing data.
from src.lib.data import items
from src.lib.data.generators.equipment import generators

from src.lib.generators.generator import Generator

class EquipmentGenerator(Generator):
    def __init__(self, choices):
        Generator.__init__(self, choices)

    def generate_equipment(self, loadout_name):
        loadout_choice, loadout_data = self.choose(loadout_name)

        # Return false if there's no match.
        if loadout_choice is None:
            return False

        # Copy information about the loadout and get the name of the item to generate.
        options = loadout_data.copy()
        items = options.pop("items", [loadout_choice])

        # Generate and return a list of items.
        equipment = []
        for item in items:
            equipment.append(generate_item(item, options))
        return equipment

class ItemGenerator(Generator):
    def __init__(self, choices):
        Generator.__init__(self, choices)

    def random_item(self, type):
        type_key, type_data = self.choose(type)
        return generate_item(type_key, type_data)

# TODO: Figure out where to move this.
def generate_item(item_name, options=None):
    item_stats = items.item_list.get(item_name)

    # Return false if there's no match.
    if item_stats is None:
        return False

    # Make a copy so we can alter it safely.
    item_stats = item_stats.copy()

    # Override with passed options.
    if options is not None:
        item_stats.update(options)

    # Generate the appropriate item - either directly or via a variant.
    variant = item_stats.get("variant")
    if variant is None:
        item = item_stats.pop("class")()
    else:
        item = generate_item(variant)

    # HACK: Set the item name.
    item.name = item_name

    # Set other attributes of the item.
    for stat, value in item_stats.items():
        setattr(item, stat, value)

    return item

def variant_item(item_stats):
    if item_stats.get("variant") is None:
        return item_stats
    else:
        variantstats = items.item_list[item_stats["variant"]].copy()
        return variant_item(variantstats)

def generate_collection(collection, item_stats):
#   collection.items

#items = item_stats["collection"]
#    exit(item_stats)#
    for item_name, stats in item_stats["collection"].items():
        collection[item_name] = generate_item(item_name)

 #  if stats.get("variant") is not None:
 #       stats = items.item_list[stats["variant"]].copy()

#    itemclass = item_stats.pop("class")
#    item = itemclass()
    return item
