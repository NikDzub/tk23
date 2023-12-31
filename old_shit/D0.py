#!/usr/bin/env python3

# python3 D0.py && python3 D1.py && python3 D2.py &&

from ppadb.client import Client as AdbClient
import time
import asyncio
import subprocess
import random


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()

if len(devices) == 0:
    quit(0)

xy_search = "685 80"


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]


print(f"\033[90m{subprocess.getoutput('adb devices -l')}\033[0m")


async def open_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    await asyncio.sleep(2)


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    for device in devices:
        await open_app(device)
        n_try = 10

        while True:
            if n_try == 0:
                device.shell("reboot -p")
                break

            try:
                output = await get_output(device)
                n_try = n_try - 1

                if "MainPageFragment" in output:
                    print("App loaded.")
                    await asyncio.sleep(1)
                    # pause main page video
                    device.shell(f"input keyevent 62")

                    while True:
                        # go to search
                        device.shell(f"input tap {xy_search}")
                        output = await get_output(device)

                        if "SearchResultFragmentNew" in output:
                            break

                    break

            except Exception as error:
                print(error)


asyncio.run(main())
