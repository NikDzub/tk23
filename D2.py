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

xy_video_01 = "100 717"
x_video_01 = 100
y_video_01 = 717

xy_video_02 = "260 717"
x_video_02 = 260
y_video_02 = 717

xy_top_follower = "378 155"

xy_bookmark = "695 1019"


async def check_if_video(device, x, y):
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

    if pixel(100, 717) == (255, 255, 255):
        return 0
    else:
        return 1


async def goto_video(device, xy_video):
    print("go to video")
    await asyncio.sleep(1)
    device.shell(f"input tap {xy_video}")
    await asyncio.sleep(1)
    device.shell(f"input keyevent {key_space}")
    device.shell(f"input tap {xy_bookmark}")
    await asyncio.sleep(1)
    device.shell(f"input keyevent {key_back}")


async def verify_in_search(device):
    n_try = 100

    while True:
        # print(n_try)
        if n_try == 0:
            # device.shell("reboot -p")
            print("Shutting down")
            break

        try:
            output = await get_output(device)
            n_try = n_try - 1

            if "FollowRelationTabFragment" in output:
                device.shell(f"input swipe 120 600 100 400")
                device.shell(f"input tap {xy_top_follower}")
                await asyncio.sleep(1)

            video_exists = await check_if_video(device, x_video_01, y_video_01)

            if video_exists:
                # print("video1 exists")
                await goto_video(device, xy_video_01)

            video_exists = await check_if_video(device, x_video_02, y_video_02)
            if video_exists:
                # print("video2 exists")
                await goto_video(device, xy_video_02)

            if "UserProfileFragment" in output:
                await asyncio.sleep(1)
                device.shell(f"input keyevent {key_back}")
                await asyncio.sleep(1)

            # now in follower profile

        except Exception as error:
            print(error)


async def quit_app(device):
    device.shell(f"am kill <PACKAGE>")


# 🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️🏄‍♀️
async def main():
    await asyncio.gather(*[verify_in_search(device) for device in devices])
    await asyncio.gather(*[quit_app(device) for device in devices])


asyncio.run(main())
