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


async def check_if_video(device):
    width = 720

    def pixel(x, y):
        device.shell("screencap /sdcard/screencap.txt")
        device.pull(
            "/sdcard/screencap.txt",
            "./trash/screen.temp",
        )
        with open("./trash/screen.temp", "rb") as f:
            byte = f.read()[12:]
            pixel = (width * y + x) * 4
            return (byte[pixel], byte[pixel + 1], byte[pixel + 2])

    if pixel(80, 665) == (255, 255, 255):
        return 0
    else:
        return 1


async def go_to_followers(device):
    while True:
        await asyncio.sleep(1)
        output = device.shell(f"dumpsys activity {app_name}")
        index_start = output.rindex("Added Fragments:")
        index_end = output.rindex("}")
        output = output[index_start:index_end]

        if "FollowRelationTabFragment" not in output:
            device.shell(f"input keyevent 4")

        else:
            break


async def book_mark(device):
    await asyncio.sleep(1)
    device.shell(f"input keyevent 62")
    await asyncio.sleep(1)
    device.shell(f"input tap 690 1015")

    await go_to_followers(device)


async def loop_followers(device):
    while True:
        video_exists = await check_if_video(device)

        if video_exists:
            print("Video Exists")
            await asyncio.sleep(1)
            device.shell(f"input tap 80 665")
            await asyncio.sleep(1)
            device.shell(f"input keyevent 62")
            await asyncio.sleep(1)

            await book_mark(device)
        else:
            await go_to_followers(device)


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    await asyncio.gather(*[loop_followers(device) for device in devices])


asyncio.run(main())
