# Fishes and fights South of Port Sarim until level 50

api = lambda: None
def set_api():
  """
  Sets all the global variables into an api variable so it can be passed to other scripts
  Avoid defining too many things in this file..
  """
  for k in globals():
    if k.startswith("__") or k == "api":
      continue
    setattr(api, k, globals()[k])

SLEEPING_BAG = 1263
TINDERBOX    = 166
BRONZE_AXE   = 87
FISHING_NET  = 376

walk_path = None
def walk_to_point(point: "List[int]", debug_name: str = "(some path)") -> int:
    global walk_path
    if walk_path == None:
      api.log("Calculating path to " + debug_name + "")
      walk_path = api.calculate_path_to(point[0], point[1])
      if walk_path == None:
        api.log("Failed to calculate path to " + debug_name + "")
        return 1000

    walk_path.process()
    if not walk_path.complete():
      api.log("Walking " + debug_name + "")
      if not walk_path.walk():
        api.log("Failed to walk " + debug_name + "")
        walk_path = None
      else:
        api.log("Walked " + debug_name + " successfully")
      return 600
    else:
      walk_path = None

    return 650

def get_adjacent_coord():
    if is_reachable(get_x()+1, get_z()):
        return (get_x()+1, get_z())
    elif is_reachable(get_x(), get_z()+1):
        return (get_x(), get_z()+1)
    elif is_reachable(get_x()-1, get_z()):
        return (get_x()-1, get_z())
    elif is_reachable(get_x(), get_z()-1):
        return (get_x(), get_z()-1)

    return (None, None)

def walk_adjacent() -> int:
    adj_x, adj_z = get_adjacent_coord()
    if adj_x == None or adj_z == None:
      api.log("FAILED TO GET ADJACENT COORD!! RIP GOOD SOUL")
      return 1000
    if api.walk_to(adj_x, adj_z):
      api.log("Moved to %s, %s" % (adj_x, adj_z))
    else:
      api.log("Failed to move to %s, %s" % (adj_x, adj_z))
    return 1000

print(api)

import skip_tutorial_script
import get_acc_builder_equip
import full_shrimp_port_sarim

move_timer = False

def loop():
    set_api() # Needs to be called on each loop because the globals get updated on login

    api.set_autologin(True)

    global move_timer
    if move_timer:
      api.log("Moving otherwise we'll log out..")
      move_timer = False
      return walk_adjacent()

    if api.get_fatigue() > 95 and api.has_inventory_item(SLEEPING_BAG):
        api.log("Sleeping zzz")
        api.use_sleeping_bag()
        return 5000

    if not skip_tutorial_script.done(api):
      api.log("Tutorial")
      return skip_tutorial_script.go(api)
    if not get_acc_builder_equip.done(api):
      api.log("Getting acc builder equip")
      return get_acc_builder_equip.go(api)
    if not full_shrimp_port_sarim.done(api):
      api.log("Fishing shrimp")
      return full_shrimp_port_sarim.go(api)
    else:
        api.log("Done everything. I have %s items in my inventory" % len(api.get_inventory_items()))
        api.stop_script()
        api.set_autologin(False)
        api.logout()
        api.stop_account()
        return 10000

def on_server_message(msg):
    global move_timer

    if msg.startswith("@cya@You have been standing"):
        move_timer = True