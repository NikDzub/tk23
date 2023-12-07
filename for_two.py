#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
from uiautomator import Device
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(0)

i = 1
device = devices[i]

width = 480


def pixel(x, y, device):
    print("sheled3434")

    device.shell(f"screencap /sdcard/screencap{i}.txt")
    print("sheled")

    device.pull(
        f"/sdcard/screencap{i}.txt",
        f"./screen{i}.temp",
    )
    with open(f"./screen{i}.temp", "rb") as f:
        byte = f.read()[12:]
        pixel = (width * y + x) * 4
        return (byte[pixel], byte[pixel + 1], byte[pixel + 2])


already_saved = 0


async def p1():
    global already_saved
    while already_saved < 10:
        device.shell("input swipe 10 149 10 0 100")
        await asyncio.sleep(0.5)
        device.shell(f"input keyevent 62")
        await asyncio.sleep(1)

        if pixel(441, 285, device) != (218, 180, 19):
            device.shell(f"input tap 447 272")
        else:
            already_saved = already_saved + 1
            print("already saved")
        await asyncio.sleep(1)


asyncio.run(p1())
