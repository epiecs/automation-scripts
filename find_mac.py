from netmiko import ConnectHandler
from dotenv import dotenv_values
import re
import yaml

env = dotenv_values()

mac_address = "0C:40:7F:C0:00:00"

def convert_cisco_mac(mac):
    re_mac = r"[\d\w]+"
    matches = re.findall(re_mac, mac)
    
    extracted_mac = "".join(matches).lower()
    
    formatted_mac = f"{extracted_mac[0:4]}.{extracted_mac[4:8]}.{extracted_mac[8:12]}"
    
    return formatted_mac

cisco_mac = convert_cisco_mac(mac_address)

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

access_switches = {hostname: config 
            for hostname, config in inventory.items() 
            if "access-switches" in config['groups']
        }

print(f"show mac address-table | include {cisco_mac}")

for hostname, config in access_switches.items():
    
    print(f"Connecting to {hostname}")
    
    network_device = {
        "device_type": "cisco_ios",
        "host": config['hostname'],
        "username": env['USERNAME'],
        "password": env['PASSWORD'],
        "secret": env['SECRET']
    }
   
    connection = ConnectHandler(**network_device)

    connection.enable()

    result = connection.send_command(f"show mac address-table | include {cisco_mac}")

    print(result)