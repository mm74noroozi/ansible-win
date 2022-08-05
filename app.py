from datetime import datetime
from yaml import safe_load as load
from pprint import pprint
from paramiko import SSHClient,AutoAddPolicy

with open("config.yml","r+") as f:
    obj=load(f.read())
    vms=obj["vms"]
    commands=obj["commands"]


pprint(vms)

sessions=[]

for item in vms:
    with SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(item["host"], username='root',port=2223,look_for_keys=True)
        print(f'\n\n----------------------{item["name"]}--------------------------')
        for command in commands:
            print("->",command)
            stdin,stdout,stderr = client.exec_command(command)
            print(stdout.read().decode("utf8"))
    print(f"------------{datetime.now()}-----------------")

