from netmiko import ConnectHandler
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader
import yaml

env = dotenv_values()

templates = Environment(
    loader=FileSystemLoader('templates')
)

template = templates.get_template("first_5.j2")

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
    connection.config_mode()
    result = connection.send_command(f"hostname {hostname.upper()}", expect_string=r"#")
    connection.find_prompt()

    config_file = template.render(
                        ntp_server="193.104.37.238"
                    ).split("\n")
    
    result = connection.send_config_set(config_file)
    result += connection.save_config()

    print(result)