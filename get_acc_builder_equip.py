# Gets sleeping bag, tinderbox, bronze axe, and small fishing net

# Pickpockets men in Lumbridge until it gets enough gold for a sleeping bag
# and then buys one.

# If there are no men in a narrow range it will wait until there is one.

MAN          = 11
SLEEPING_BAG = 1263
TINDERBOX    = 166
BRONZE_AXE   = 87
FISHING_NET  = 376
COINS        = 10
SHOP_NPCS    = [83, 55]
THEIV_PT     = (128, 641)
SHOP_PT      = (133, 643)
BOB_PT       = (122, 668)
BOB_ID       = 1
FISH_SHOP_NPC = 167
FISH_STORE_PT = (277, 649)

to_coins_path = None
to_generalstore_path = None
to_bob_path = None
to_fishing_store_path = None

def loop():
    if get_x() == 0:
      log("GET_X IS 0 in get_acc_builder")
    if done():
        log("finished objective")
        return 10000
    return go()

def done(api):
    return api.has_inventory_item(SLEEPING_BAG) and api.has_inventory_item(TINDERBOX) and api.has_inventory_item(BRONZE_AXE) and api.has_inventory_item(FISHING_NET)

def go(api):
    if api.in_combat():
        if not api.walk_to(api.get_x(), api.get_z()):
          api.log("Could not escape combat")
        return 650

    if drop_unneeded_items(api):
        return 700

    coin_count = api.get_inventory_count_by_id(COINS)
    api.log("# Coins = %d. Has sleeping bag = %s. Has tinderbox = %s. Has bronze axe = %s. Has net = %s" % (coin_count, api.has_inventory_item(SLEEPING_BAG), api.has_inventory_item(TINDERBOX), api.has_inventory_item(BRONZE_AXE), api.has_inventory_item(FISHING_NET)))
    
    if coin_count >= 39 and not api.has_inventory_item(SLEEPING_BAG): 
        return buy_sleeping_bag(api)
    elif coin_count >= 1 and not api.has_inventory_item(TINDERBOX) and api.has_inventory_item(SLEEPING_BAG):
        return buy_tinderbox(api)
    elif coin_count >= 16 and not api.has_inventory_item(BRONZE_AXE) and api.has_inventory_item(TINDERBOX):
        return buy_bronze_axe(api)
    elif coin_count >= 5 and not api.has_inventory_item(FISHING_NET) and api.has_inventory_item(BRONZE_AXE):
        return buy_fishing_net(api)
    else:
        return get_coins(api)
    
    return 700

def drop_unneeded_items(api):
    for item in api.get_inventory_items():
        if item.id != SLEEPING_BAG and item.id != TINDERBOX and item.id != BRONZE_AXE and item.id != COINS and item.id != FISHING_NET:
            api.drop_item(item)
            return True
    return False

def get_coins(api):
    global to_coins_path
    if not api.in_radius_of(THEIV_PT[0],THEIV_PT[1],8):
        # use calculate_path_to to get to the center of the theiving area
        if to_coins_path != None:
          to_coins_path.process()
          if not to_coins_path.complete():
            api.log("Walking to_coins_path")
            if not to_coins_path.walk():
              api.log("Failed to walk to_coins_path")
              to_coins_path = None
            return 600
          else:
            to_coins_path = None

        if api.get_x() != THEIV_PT[0] or api.get_z() != THEIV_PT[1]:
          api.log("Calculating path to_coins_path")
          to_coins_path = api.calculate_path_to(THEIV_PT[0], THEIV_PT[1])
          if to_coins_path == None:
            api.log("Could not find path to_coins_path from (%d, %d) to (%d, %d)" % (api.get_x(), api.get_z(), THEIV_PT[0], THEIV_PT[1]))
            return 1000
        return 5000

    # Check if any of the items we need are on the ground
    for id in [SLEEPING_BAG, TINDERBOX, BRONZE_AXE, FISHING_NET]:
        ground_item = api.get_nearest_ground_item_by_id(id, x=THEIV_PT[0], z=THEIV_PT[1], radius=8, reachable=True)
        if ground_item != None:
            api.pickup_item(ground_item)
            return 700
    
    man = api.get_nearest_npc_by_id(MAN, in_combat=False, reachable=True, x=THEIV_PT[0], z=THEIV_PT[1], radius=8)
    if man != None:
        api.thieve_npc(man)

    return 700

def buy_sleeping_bag(api):
    global to_generalstore_path

    if not api.in_radius_of(SHOP_PT[0],SHOP_PT[1],8):
        # use calculate_path_to to get to SHOP_PT
        if to_generalstore_path != None:
          to_generalstore_path.process()
          if not to_generalstore_path.complete():
            api.log("Walking to_generalstore_path")
            if not to_generalstore_path.walk():
              api.log("Failed to walk to_generalstore_path")
              to_generalstore_path = None
            return 600
          else:
            to_generalstore_path = None

        if api.get_x() != SHOP_PT[0] or api.get_z() != SHOP_PT[1]:
          api.log("Calculating path to_generalstore_path")
          to_generalstore_path = api.calculate_path_to(SHOP_PT[0], SHOP_PT[1])
          if to_generalstore_path == None:
            api.log("failed to path with to_generalstore_path")
            return 1000

        return 650

    if api.in_radius_of(132, 641, 15):
        door = api.get_wall_object_from_coords(132, 641)
        if door != None and door.id == 2:
            api.at_wall_object(door)
            return 1300

    if not api.is_shop_open():
        if api.is_option_menu():
            api.answer(0)
            return 3000
        else:
            npc = api.get_nearest_npc_by_id(ids=SHOP_NPCS, talking=False, reachable=True)
            if npc != None:
                api.talk_to_npc(npc)
                return 3000
    else:
        api.buy_shop_item(SLEEPING_BAG, 1)
    
    return 3000

def buy_tinderbox(api):
    global to_generalstore_path

    if not api.in_radius_of(SHOP_PT[0],SHOP_PT[1],8):
        # use calculate_path_to to get to SHOP_PT
        if to_generalstore_path != None:
          to_generalstore_path.process()
          if not to_generalstore_path.complete():
            api.log("Walking to_generalstore_path")
            if not to_generalstore_path.walk():
              api.log("Failed to walk to_generalstore_path")
              to_generalstore_path = None
            return 600
          else:
            to_generalstore_path = None

        if api.get_x() != SHOP_PT[0] or api.get_z() != SHOP_PT[1]:
          api.log("Calculating path to_generalstore_path")
          to_generalstore_path = api.calculate_path_to(SHOP_PT[0], SHOP_PT[1])
          if to_generalstore_path == None:
            api.log("failed to path with to_generalstore_path")
            return 1000

        return 650

    if api.in_radius_of(132, 641, 15):
        door = api.get_wall_object_from_coords(132, 641)
        if door != None and door.id == 2:
            api.at_wall_object(door)
            return 1300

    if not api.is_shop_open():
        if api.is_option_menu():
            api.answer(0)
            return 3000
        else:
            npc = api.get_nearest_npc_by_id(ids=SHOP_NPCS, talking=False, reachable=True)
            if npc != None:
                api.talk_to_npc(npc)
                return 3000
    else:
        api.buy_shop_item(TINDERBOX, 1)

    return 3000

def buy_bronze_axe(api):
    global to_bob_path

    if not api.in_radius_of(BOB_PT[0],BOB_PT[1],3):
        # use calculate_path_to to get to BOB_PT
        if to_bob_path != None:
          to_bob_path.process()
          if not to_bob_path.complete():
            api.log("Walking to_bob_path")
            if not to_bob_path.walk():
              api.log("Failed to walk to_bob_path")
              to_bob_path = None
            return 600
          else:
            to_bob_path = None

        if api.get_x() != BOB_PT[0] or api.get_z() != BOB_PT[1]:
          api.log("Calculating path to BOB_PT")
          to_bob_path = api.calculate_path_to(BOB_PT[0], BOB_PT[1])
          if to_bob_path == None:
            api.log("failed to path with to_bob_path")
            return 1000

        return 650

    if not api.is_shop_open():
        if api.is_option_menu():
            api.answer(1)
            return 3000
        else:
            npc = api.get_nearest_npc_by_id(ids=[BOB_ID], talking=False, reachable=True)
            if npc != None:
                api.talk_to_npc(npc)
                return 3000
    else:
        api.buy_shop_item(BRONZE_AXE, 1)

    return 3000

def buy_fishing_net(api):
  global to_fishing_store_path

  if not api.in_radius_of(FISH_STORE_PT[0],FISH_STORE_PT[1],8):
    # use calculate_path_to to get to FISH_STORE_PT
    if to_fishing_store_path != None:
      to_fishing_store_path.process()
      if not to_fishing_store_path.complete():
        api.log("Walking to_fishing_store_path")
        if not to_fishing_store_path.walk():
          api.log("Failed to walk to_fishing_store_path")
          to_fishing_store_path = None
        return 600
      else:
        to_fishing_store_path = None

    if api.get_x() != FISH_STORE_PT[0] or api.get_z() != FISH_STORE_PT[1]:
      api.log("Calculating path to FISH_STORE_PT")
      to_fishing_store_path = api.calculate_path_to(FISH_STORE_PT[0], FISH_STORE_PT[1])
      if to_fishing_store_path == None:
        api.log("failed to path with to_fishing_store_path")
        return 1000

    return 650
  
  if not api.is_shop_open():
    if api.is_option_menu():
      api.answer(0)
      return 3000
    else:
      npc = api.get_nearest_npc_by_id(ids=[FISH_SHOP_NPC], talking=False, reachable=True)
      if npc != None:
        api.talk_to_npc(npc)
        return 3000
  else:
    api.buy_shop_item(FISHING_NET, 1)

  return 3000

