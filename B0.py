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


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()

if len(devices) == 0:
    print("No devices")
    quit(0)


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
            print(n_try)
            if n_try == 0:
                device.shell("reboot -p")
                break

            try:
                await asyncio.sleep(1)
                output = device.shell(f"dumpsys activity {app_name}")
                index_start = output.rindex("Added Fragments:")
                index_end = output.rindex("}")
                output = output[index_start:index_end]

                n_try = n_try - 1

                if "MainPageFragment" in output:
                    print("App loaded.")
                    break

            except Exception as error:
                print(error)


asyncio.run(main())
