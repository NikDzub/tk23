import asyncio
from ppadb.client import Client as AdbClient
import os
import shutil
import json


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()

if len(devices) == 0:
    print("No devices")
    quit(0)


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    print(output[index_start:index_end])
    return output[index_start:index_end]


async def main():
    while True:
        await get_output(devices[0])


asyncio.run(main())
