from . import PowerwallController
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('measurement', choices=['charge', 'battery', 'solar', 'grid', 'house', 'connected'])
args = parser.parse_args()

con = PowerwallController(args.host)

if args.measurement == 'charge':
  method = con.get_battery_charge
elif args.measurement == 'battery':
  method = con.get_battery_power
elif args.measurement == 'solar':
  method = con.get_solar_power
elif args.measurement == 'grid':
  method = con.get_grid_power
elif args.measurement == 'house':
  method = con.get_house_power
elif args.measurement == 'connected':
  method = con.is_grid_connected
else:
  raise Exception("invalid option")

print(method())