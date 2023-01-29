from netmiko import ConnectHandler
from dotenv import dotenv_values

env = dotenv_values()

sw_acc_1 = {
    "device_type": "cisco_ios",
    "host": "10.0.90.11",
    "username": env['USERNAME'],
    "password": env['PASSWORD'],
    "secret": env['SECRET']
}

connection = ConnectHandler(**sw_acc_1)

# result = connection.send_command(
#     "show version | include Version"
# )

# Werkt niet zonder enable
connection.enable()
result = connection.send_command(
    "show running-config interface GigabitEthernet 0/0"
)

print(result)