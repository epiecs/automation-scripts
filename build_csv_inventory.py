from netmiko import ConnectHandler
from dotenv import dotenv_values
import re
import csv
import yaml

env = dotenv_values()

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

# Match alles achter het woord Version tot aan de volgende whitespace of komma
re_version = r"Version\s(?P<version>[^\s,]+)"

audit_inventory = []

for hostname, config in inventory.items():
    
    print(f"Connecting to {hostname}")
    
    network_device = {
        "device_type": "cisco_ios",
        "host": config['hostname'],
        "username": env['USERNAME'],
        "password": env['PASSWORD'],
        "secret": env['SECRET']
    }
   
    connection = ConnectHandler(**network_device)

    result = connection.send_command(
        "show version"
    )

    matches = re.search(re_version, result)

    audit_inventory.append({
        "type": config['groups'][0],
        "hostname": hostname,
        "ip": config['hostname'],
        "version": matches.group('version')
    })
    
        
with open('build_csv_inventory.csv', 'w') as csv_file:
    inventory_writer = csv.DictWriter(csv_file, 
                                      fieldnames=("type", "hostname", "ip", "version")
                                      )
    
    inventory_writer.writeheader()
    for device in audit_inventory:
        inventory_writer.writerow(device)
