from netmiko import ConnectHandler
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader
import yaml

env = dotenv_values()

templates = Environment(
    loader=FileSystemLoader('templates')
)

template = templates.get_template("vlans.j2")

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

    config_file = template.render(
                        **config
                    ).split("\n")
    
    connection.enable()
    result = connection.send_config_set(config_file)
    result += connection.save_config()

    print(result)