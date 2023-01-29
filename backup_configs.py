from netmiko import ConnectHandler
from dotenv import dotenv_values
import os
import yaml

env = dotenv_values()

backup_folder = "config_backups"

try:
    os.mkdir(backup_folder)
except FileExistsError as error:
    print("Directory already exists")   

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

for hostname, config in inventory.items():
    
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
    running_config = connection.send_command("show run | begin version")
    
    with open(f"{backup_folder}/{hostname}.ios", "w") as config_file:
        config_file.write(running_config)