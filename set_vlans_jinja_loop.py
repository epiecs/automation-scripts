from netmiko import ConnectHandler
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader
import yaml

env = dotenv_values()

templates = Environment(
    loader=FileSystemLoader('templates')
)

template = templates.get_template("vlans_loop.j2")

vlans_config = {
    "10": "it",
    "20": "corp",
    "90": "mgmt",
    "99": "native"
}

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
        "secret": env['SECRET']
    }
    
    connection = ConnectHandler(**network_device)

    config_file = template.render(
                        vlans=vlans_config
                    ).split("\n")
        
    connection.enable()
    result = connection.send_config_set(config_file)
    result += connection.save_config()

    print(result)