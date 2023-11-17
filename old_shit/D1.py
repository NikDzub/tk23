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

users = []

with open("users.txt", "r", encoding="utf-8") as f:
    users = f.readlines()


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]


key_enter = 66
key_space = 62
key_back = 4
key_down = 20
key_up = 19
key_tab = 61

xy_users_tab = "250 145"

xy_top_result = "328 230"


async def verify_in_search(device):
    n_try = 5

    while True:
        if n_try == 0:
            # device.shell("reboot -p")
            print("Shutting down")
            break

        try:
            output = await get_output(device)
            n_try = n_try - 1

            if "SearchResultFragmentNew" in output:
                print("In Search.")
                await asyncio.sleep(1)
                device.shell(f"input text {random.choice(users)}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_enter}")
                await asyncio.sleep(2)
                device.shell(f"input tap {xy_users_tab}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_enter}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_down}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_down}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_enter}")

            if "UserProfileFragment" in output:
                print(f"In Profile")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_tab}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_up}")
                await asyncio.sleep(1)
                # get top highlighted
                device.shell(f"input keyevent {key_up}")
                device.shell(f"input keyevent {key_up}")
                device.shell(f"input keyevent {key_up}")
                device.shell(f"input keyevent {key_up}")
                device.shell(f"input keyevent {key_up}")
                await asyncio.sleep(1)

                device.shell(f"input keyevent {key_down}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_down}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_down}")
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_enter}")

            if "FollowRelationTabFragment" in output:
                print(f"In Followers")
                await asyncio.sleep(1)

                break
            # now in follower profile

        except Exception as error:
            print(error)


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    await asyncio.gather(*[verify_in_search(device) for device in devices])


asyncio.run(main())
