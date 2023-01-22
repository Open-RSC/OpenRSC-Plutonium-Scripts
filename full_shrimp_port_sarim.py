# Fills inventory with cooked shrimp South West of port Sarim

# get_acc_builder_equip should be run first to get all the reqs

BURNT_SHRIMP_ID = 353
RAW_SHRIMP_ID = 349
RAW_ANCHOVY_ID = 321
COOKED_SHRIMP_ID = 350
TINDERBOX_ID = 166
LOGS_ID = 14
TREE_IDS = [0, 1]
FISH_SPOT = (310, 686)
FISH_OBJ_ID = 193
FIRE_ID = 97

unstuck = False

def done(api):
    return len(api.get_inventory_items()) >= 25 and not api.has_inventory_item(BURNT_SHRIMP_ID) and not api.has_inventory_item(RAW_SHRIMP_ID) and not api.has_inventory_item(RAW_ANCHOVY_ID)

def go(api):
    global unstuck
    if api.in_combat():
        if not api.walk_to(api.get_x(), api.get_z()):
          api.log("Could not escape combat")
        return 650

    api.log("# Cooked shrimp = %s, # Raw shrimp = %s" % (api.get_inventory_count_by_id(COOKED_SHRIMP_ID), api.get_inventory_count_by_id(RAW_SHRIMP_ID)))

    if unstuck:
        return get_unstuck(api)
    elif len(api.get_inventory_items()) < 25:
        return go_fish(api)
    elif api.has_inventory_item(RAW_SHRIMP_ID) and api.get_nearest_object_by_id(FIRE_ID):
        return cook_shrimp(api)
    elif api.get_nearest_ground_item_by_id(LOGS_ID):
        return burn_logs(api)
    elif api.has_inventory_item(LOGS_ID):
        return drop_logs(api)
    else:
        return chop_logs(api)

    return 700

def get_unstuck(api):
    global unstuck
    unstuck = False
    log("Getting unstuck")
    return api.walk_path_point((305, 880), "firemakable location")

def drop_unneeded_items(api):
    for item in api.get_inventory_items():
        if item.id == BURNT_SHRIMP_ID or item.id == RAW_ANCHOVY_ID:
            api.drop_item(item)
            return True
    return False

def go_fish(api):
    if drop_unneeded_items(api):
        return 700

    if not api.in_radius_of(FISH_SPOT[0],FISH_SPOT[1],8):
        return api.walk_to_point(FISH_SPOT, "fish spot")

    fish_spot_obj = api.get_nearest_object_by_id(FISH_OBJ_ID)
    if fish_spot_obj == None:
        api.log("Could not find fishing spot")
        return 1000

    api.at_object(fish_spot_obj)

    return 2000

def cook_shrimp(api):
    fire_obj = api.get_nearest_object_by_id(FIRE_ID)
    if fire_obj == None:
        api.log("Could not find fire")
        return 1000

    api.log("Gonna use " + str(api.get_inventory_item_by_id(RAW_SHRIMP_ID)) + " on " + str(fire_obj))
    api.use_item_on_object(api.get_inventory_item_by_id(RAW_SHRIMP_ID), fire_obj)

    return 2000

def burn_logs(api):
    logs = api.get_nearest_ground_item_by_id(LOGS_ID)
    if logs == None:
        api.log("Could not find logs")
        return 1000

    api.use_item_on_ground_item(api.get_inventory_item_by_id(TINDERBOX_ID), logs)

    return 2000

def drop_logs(api):
    api.drop_item(api.get_inventory_item_by_id(LOGS_ID))

    return 2000

def chop_logs(api):
    if drop_unneeded_items(api):
        return 700

    tree = api.get_nearest_object_by_id(ids=TREE_IDS)
    if tree == None:
        api.log("Could not find tree")
        return 1000

    api.at_object(tree)

    return 2000


def on_server_message(msg):
    global unstuck

    if msg.startswith("You can't light"):
        log("Need to get unstuck")
        unstuck = True