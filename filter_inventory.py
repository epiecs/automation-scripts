from netmiko import ConnectHandler
from dotenv import dotenv_values
import re
import yaml

env = dotenv_values()

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)


routers = {hostname: settings 
           for hostname, settings in inventory.items()
           if "routers" in settings['groups']
           }

print(routers)

# >>>
# {
# 'r1': {'hostname': '10.0.100.11', 'groups': ['routers']}, 
# 'r2': {'hostname': '10.0.100.12', 'groups': ['routers']}
# }