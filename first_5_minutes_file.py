from netmiko import ConnectHandler
from dotenv import dotenv_values
import yaml

env = dotenv_values()

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

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

    connection.enable()

    result = connection.send_config_from_file("first_5_config.ios")
    
    result += connection.save_config()

    print(result)
