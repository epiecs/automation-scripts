from netmiko import ConnectHandler

sw_acc_1 = {
    "device_type": "cisco_ios",
    "host": "10.0.90.11",
    "username": "admin",
    "password": "Appel.Sap1",
    "secret": "Acti.Vate",
    "session_log": "session.log"
}

connection = ConnectHandler(**sw_acc_1)

result = connection.send_command(
    "show version | include Version"
)

# Werkt niet zonder enable
connection.enable()
result = connection.send_command(
    "show running-config interface GigabitEthernet 0/0"
)

print(result)