from netmiko import ConnectHandler
from dotenv import dotenv_values
from jinja2 import Environment, FileSystemLoader
import yaml

env = dotenv_values()

templates = Environment(
    loader=FileSystemLoader('templates')
)

template = templates.get_template("first_template.j2")

with open('inventory.yaml', 'r') as inventory_file:
    inventory = yaml.safe_load(inventory_file)

for hostname, config in inventory.items():
    print(template.render(name=hostname))