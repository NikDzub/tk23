#!/usr/bin/env python3

from ppadb.client import Client as AdbClient
import time
import asyncio
import subprocess
import random


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
    return output[index_start:index_end]


async def loop_followers(device):
    while True:
        output = await get_output(device)

        if "FollowRelationTabFragment" in output:
            device.shell(f"input keyevent 20")
            await asyncio.sleep(1)
            device.shell(f"input keyevent 66")

        if "UserProfileFragment" in output:
            await asyncio.sleep(1)
            device.shell(f"input keyevent 4")


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    await asyncio.gather(*[loop_followers(device) for device in devices])


asyncio.run(main())
