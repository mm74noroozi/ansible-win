from asyncio.log import logger
from datetime import datetime
import asyncio
from yaml import safe_load as load
from pprint import pprint
from paramiko import SSHClient,AutoAddPolicy
import logging


logging.basicConfig(format='%(asctime)s - %(name)s: %(message)s',level=logging.INFO)

with open("config.yml","r+") as f:
    obj=load(f.read())
    vms=obj["vms"]
    commands=obj["commands"]



async def run_commands(vm,commands):
    logger=logging.getLogger(vm["name"])
    with SSHClient() as client:
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(vm["host"], username='root',port=2223,look_for_keys=True)
        for command in commands:
            logger.info("->"+command)
            _,stdout,__ = client.exec_command(command)
            logger.info(stdout.read().decode("utf8"))

async def main():
    jobs=[asyncio.create_task(run_commands(vm,commands)) for vm in vms]
    await asyncio.gather(*jobs)

if __name__ == "__main__":
    asyncio.run(main())
