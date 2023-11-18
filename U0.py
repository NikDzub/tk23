#!/usr/bin/env python3
from ppadb.client import Client as AdbClient
import time
import asyncio
import subprocess
import random
import json
import sys

# adb shell am start -W -a android.intent.action.VIEW -d "https://www.tiktok.com/@therock" com.zhiliaoapp.musically

client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(1)
device = devices[0]

app_name = "com.zhiliaoapp.musically"
all_layers = f"dumpsys activity {app_name}"


user = sys.argv[1]

print(user)


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]
