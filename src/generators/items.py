from data import items

def generate_item(itemname):
    itemstats = items.item_list[itemname].copy()
    variant = itemstats.get("variant")
    if variant is None:
        item = itemstats.pop("class")()
    else:
        item = generate_item(variant)

    item.name = itemname

    if itemstats.get("collection") is not None:
        generate_collection(item, itemstats)
    else:
        for stat, value in itemstats.items():
            setattr(item, stat, value)
    return item

def variant_item(itemstats):
    if itemstats.get("variant") is None:
        return itemstats
    else:
        variantstats = items.item_list[itemstats["variant"]].copy()
        return variant_item(variantstats)

def generate_collection(collection, itemstats):
#   collection.items

#items = itemstats["collection"]
#    exit(itemstats)#
    for itemname, stats in itemstats["collection"].items():
        collection[itemname] = generate_item(itemname)

 #  if stats.get("variant") is not None:
 #       stats = items.item_list[stats["variant"]].copy()

#    itemclass = itemstats.pop("class")
#    item = itemclass()
    return item
