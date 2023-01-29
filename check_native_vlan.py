from netmiko import ConnectHandler
from dotenv import dotenv_values
import re
import yaml

env = dotenv_values()

native_vlan = "99"

# Match alles achter het woord Version tot aan de volgende whitespace of komma
re_interface = r"^(?P<interface>[\w-]+)"
re_native_vlan = r"native\svlan\s(?P<nativevlan>[0-9]+)"

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

switches = {hostname: config 
            for hostname, config in inventory.items() 
            if "switches" in config['groups']
        }

for hostname, config in switches.items():
    
    print(f"Connecting to {hostname}")
    
    network_device = {
        "device_type": "cisco_ios",
        "host": config['hostname'],
        "username": env['USERNAME'],
        "password": env['PASSWORD'],
        "secret": env['SECRET'],
        "read_timeout_override": 30
    }
   
    connection = ConnectHandler(**network_device)

    connection.enable()

    result = connection.send_command("show run | section interface")

    raw_interfaces = result.split('interface ')

    for interface in raw_interfaces:
        native_vlan_search = re.search(re_native_vlan, interface)

        if native_vlan_search:
            interface_search = re.search(re_interface, interface)
            
            interface_native_vlan = native_vlan_search.groups('nativevlan')[0]
            interface_name = interface_search.groups('interface')[0]
            
            if interface_native_vlan != native_vlan:
                print(f"{hostname}::{interface_name} has wrong native vlan {interface_native_vlan}")

            