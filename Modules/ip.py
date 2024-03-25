import main
import os
from requests import get
import time

def Init(module: main.Module):
    module.color = '1010101'

def Update(module: main.Module):
    # Check if not a timer for the module is set
    ip_path = "module_data/ip/timer.txt"
    last_ip_path = "module_data/ip/last_ip.txt"
    if not os.path.exists(ip_path):
        os.makedirs(os.path.dirname(ip_path), exist_ok=True)
        with open(ip_path, 'w') as file:
            file.write(str(time.time()))
    elif not os.path.exists(last_ip_path):
        os.makedirs(os.path.dirname(last_ip_path), exist_ok=True)
        with open(last_ip_path, 'w') as file2:
            try:
                file2.write(get('https://api64.ipify.org', timeout=2).text) 
            except:
                file2.write("Error")
    else:
        # If a timer is set, check if the last time the ip was checked was longer than 180 Seconds ago, if yes -> check ip    
        with open(ip_path, 'r') as file3:
            last_update = (file3.read())
            if time.time() - float(last_update) > 180:
                try:
                    ip = (get('https://api64.ipify.org', timeout=2).text)
                except:
                    ip = "Error"
                with open(ip_path, "w") as file4:
                    file4.write(str(time.time()))  # Write the current timestamp to ip_path
                with open(last_ip_path, "w") as file5:
                    file5.write(ip)  # Write the IP address to last_ip_path
                module.full_text = "IP: " + ip

            else:
                with open(last_ip_path, "r") as file5:
                    ip = file5.read()
                module.full_text = "IP: " + ip