from netmiko import ConnectHandler
from dotenv import dotenv_values
import re

env = dotenv_values()

switches = {
    "sw_acc_1": "10.0.90.11",
    "sw_acc_2": "10.0.90.12",
    "sw_acc_3": "10.0.90.13",
    "sw_acc_4": "10.0.90.14",
}

re_interfaces = r"(?P<name>^[\w/-]+)\s+(?P<ip>[0-9\.]+)"

for hostname, ip in switches.items():
    
    print(f"Connecting to {hostname}")
    
    switch = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": env['USERNAME'],
        "password": env['PASSWORD'],
        "secret": env['SECRET']
    }

    connection = ConnectHandler(**switch)

    result = connection.send_command(
        "show ip interface brief | include 10"
    )

    for interface in re.finditer(re_interfaces, result):
        print(f"Switch {hostname} heeft interface {interface['name']} met ip {interface['ip']}")
        
