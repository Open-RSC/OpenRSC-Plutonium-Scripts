# Fishes and fights South of Port Sarim until level 50

api = lambda: None
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
        api.log("failed to path with to_generalstore_path")
        return 1000

    walk_path.process()
    if not walk_path.complete():
      api.log("Walking " + debug_name + "")
      if not walk_path.walk():
        api.log("Failed to walk " + debug_name + "")
        walk_path = None
      return 600
    else:
      walk_path = None

    return 650

setattr(api, "walk_to_point", walk_to_point)

print(api)
print()

import skip_tutorial
import get_acc_builder_equip
import full_shrimp_port_sarim

def loop():
    if api.get_x() == 0:
      api.log("GET_X IS 0 in get_base")
      api.logout()
      return 6 * 60 * 1000

    api.set_autologin(True)


    if api.get_fatigue() > 95 and api.has_inventory_item(SLEEPING_BAG):
        api.log("Sleeping zzz")
        api.use_sleeping_bag()
        return 5000

    if not skip_tutorial.done(api):
      api.log("Tutorial")
      return skip_tutorial.go(api)
    if not get_acc_builder_equip.done(api):
      api.log("Getting acc builder equip")
      return get_acc_builder_equip.go(api)
    if not full_shrimp_port_sarim.done(api):
      api.log("Fishing shrimp")
      return full_shrimp_port_sarim.go(api)
    else:
        api.log("Done everything. I have " + len(api.get_inventory_items()) + " items in my inventory")
        api.log()
        api.stop_script()
        api.set_autologin(False)
        api.logout()
        api.stop_account()
        return 10000
