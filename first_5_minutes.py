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

    connection.config_mode()
    result = connection.send_command(f"hostname {hostname.upper()}", expect_string=r"#")
    connection.find_prompt()

    commands = [
        "no logging console",                        # disable console logging
        "service password-encryption",               # encrypt passwords
        "no ip http server",                         # disable http server
        "ntp server 45.87.78.35",                    # be.pool.ntp.org
        "#login block-for 120 attempts 3 within 60"  # block 120s if 3 failed logins in 60s
    ]

    result += connection.send_config_set(commands)
    
    banner = """
        banner motd ~\n
        ----------------------------------\n
        - no unauthorized access allowed -\n
        ----------------------------------\n
        ~\n
    """
    
    # cmd_verfify is nodig omdat netmiko anders de prompt niet vindt
    result += connection.send_config_set(banner, cmd_verify=False)
    result += connection.save_config()

    print(result)
    
# >>>
# Connecting to sw-acc-4
# configure terminal
# Enter configuration commands, one per line.  End with CNTL/Z.
# SW-ACC-4(config)#hostname SW-ACC-4
# SW-ACC-4(config)#service password-encryption
# SW-ACC-4(config)#no ip http server
# SW-ACC-4(config)#ntp server 45.87.78.35
# SW-ACC-4(config)##login block-for 120 attempts 3 within 60
# SW-ACC-4(config)#end
# SW-ACC-4#configure terminal
# Enter configuration commands, one per line.  End with CNTL/Z.
# SW-ACC-4(config)#
# SW-ACC-4(config)#        banner motd ~
# Enter TEXT message.  End with the character '~'.
# 
#         ----------------------------------
# 
#         - no unauthorized access allowed -
# 
#         ----------------------------------
# 
#         ~
# SW-ACC-4(config)#end
# SW-ACC-4#write mem
# Building configuration...
# Compressed configuration from 4254 bytes to 2309 bytes[OK]
# SW-ACC-4#