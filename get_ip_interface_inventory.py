from netmiko import ConnectHandler
from dotenv import dotenv_values
import re
import yaml

env = dotenv_values()

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

re_interfaces = r"(?P<name>^[\w/-]+)\s+(?P<ip>[0-9\.]+)"

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
        "show ip interface brief | include 10"
    )

    for interface in re.finditer(re_interfaces, result):
        print(f"Apparaat {hostname} heeft interface {interface['name']} met ip {interface['ip']}")