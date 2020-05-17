import requests
import json

protocol = "https://"
base_api_path = "/api"
battery_level_path = base_api_path + "/system_status/soe"
power_levels_path = base_api_path + "/meters/aggregates"
grid_connected_path = base_api_path + "/system_status/grid_status"

class PowerwallController:
  def __init__(self, host):
    self.base_url = protocol + host

  def request_api(self, path):
    req = requests.get(self.base_url + path, verify=False)
    content = req.content.decode("utf-8")
    return json.loads(content)

  def get_battery_charge(self):
    result = self.request_api(battery_level_path)
    val = int(result['percentage'])
    return f"The battery is at {val} percent"

  def get_battery_power(self):
    result = self.request_api(power_levels_path)
    val = int(result['battery']['instant_power'])
    if val == 0:
      return "The battery is not being used"
    if val < 0:
      return f"The battery is charging at {-val} watts"
    else:
      return f"The battery is supplying {val} watts"

  def get_solar_power(self):
    result = self.request_api(power_levels_path)
    val = int(result['solar']['instant_power'])
    return f"The solar panels are supplying {val} watts"

  def get_grid_power(self):
    result = self.request_api(power_levels_path)
    val = int(result['site']['instant_power'])
    if val == 0:
      return "The grid is not being used"
    if val < 0:
      return f"You are exporting {-val} watts"
    else:
      return f"You are importing {val} watts"

  def get_house_power(self):
    result = self.request_api(power_levels_path)
    val = int(result['load']['instant_power'])
    return f"The house is using {val} watts"

  def is_grid_connected(self):
    result = self.request_api(grid_connected_path)
    val = result['grid_status']
    if val == "SystemGridConnected":
      return "The house is connected to the grid"
    elif val == "SystemIslandedActive":
      return "The house is not connected to the grid"
    elif val == "SystemTransitionToGrid":
      return "The house is connecting to the grid"
    else:
       raise Exception("The powerwall returned an unknown status")
