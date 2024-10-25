from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.184"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0

        interface_status = []


        result = ssh.send_command("show ip interface brief", use_textfsm=True)

        for status in result:
            interface_name = status['interface']  # ชื่อของ interface
            interface_state = status['status']    # สถานะของ interface
            
            interface_status.append(f"{interface_name} {interface_state}")

            if interface_state:
                #<!!!Write code here!!!>
                if interface_state == "up":
                    up += 1
                elif interface_state == "down":
                    down += 1
                elif interface_state == "administratively down":
                    admin_down += 1
        ans = f"{', '.join(interface_status)} -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans
