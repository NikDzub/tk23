#!/usr/bin/env python3

from ppadb.client import Client as AdbClient
import time
import asyncio
import subprocess
import random


# "\033[0m",
# "\033[95m",
# "\033[94m",
# "\033[96m",
# "\033[92m",
# "\033[93m",
# "\033[91m",

users = ["bellapoarch", "therock", "mcbella", "rodionova_34", "yuliacohen1"]


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()

if len(devices) == 0:
    print("No devices")
    quit(0)


async def verify_in_search(device):
    n_try = 5

    while True:
        # print(n_try)
        if n_try == 0:
            # device.shell("reboot -p")
            print("Shutting down")
            break

        try:
            await asyncio.sleep(1)
            output = device.shell(f"dumpsys activity {app_name}")
            index_start = output.rindex("Added Fragments:")
            index_end = output.rindex("}")
            output = output[index_start:index_end]

            n_try = n_try - 1

            if "SearchResultFragmentNew" in output:
                print("In Search.")
                await asyncio.sleep(1)
                device.shell(f"input text {random.choice(users)}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 66")
                await asyncio.sleep(2)
                device.shell(f"input tap 290 120")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 66")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 66")

            if "UserProfileFragment" in output:
                print(f"In Profile")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 61")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 19")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 19")
                device.shell(f"input keyevent 19")

                device.shell(f"input keyevent 19")
                device.shell(f"input keyevent 19")
                device.shell(f"input keyevent 19")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 66")

            if "FollowRelationTabFragment" in output:
                print(f"In Followers")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 20")
                await asyncio.sleep(1)
                device.shell(f"input keyevent 66")
                await asyncio.sleep(1)

                break

        except Exception as error:
            print(error)


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    await asyncio.gather(*[verify_in_search(device) for device in devices])


asyncio.run(main())
