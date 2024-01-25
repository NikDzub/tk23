#!/usr/bin/env python3

# ui.dump("hierarchy.xml")

import asyncio
from playwright.async_api import async_playwright
from uiautomator import device as ui
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(0)

i = 0
device = devices[i]
ui_search = "com.zhiliaoapp.musically:id/d4s"
ui_vid = "com.zhiliaoapp.musically:id/nom"


hash_tags = ["fyp", "parati", "edit"]


def pixel(x, y, device):
    device.shell(f"screencap /sdcard/screencap{i}.txt")
    device.pull(
        f"/sdcard/screencap{i}.txt",
        f"./screen{i}.temp",
    )
    with open(f"./screen{i}.temp", "rb") as f:
        byte = f.read()[12:]
        pixel = (480 * y + x) * 4
        return (byte[pixel], byte[pixel + 1], byte[pixel + 2])


async def book_loop():
    already_saved = 0
    while already_saved < 10:
        device.shell("input swipe 10 149 10 0 100")
        await asyncio.sleep(0.5)
        device.shell(f"input keyevent 62")
        await asyncio.sleep(1)
        if pixel(441, 285, device) != (218, 180, 19):
            device.shell(f"input tap 447 272")
        else:
            already_saved = already_saved + 1
            if already_saved == 10:
                device.shell(f"input keyevent 4")
        await asyncio.sleep(1)


async def in_search(hash_tag):
    ui(resourceId=ui_search).click()
    device.shell(f"input keyevent --longpress 67 67 67 67 67 67 67 67 67 67")
    device.shell(f"input text '{hash_tag}'")
    device.shell(f"input keyevent 66")
    for i in range(2):
        ui(resourceId=ui_search).click()
        await asyncio.sleep(1)
        device.shell(f"input keyevent 66")
    ui(text="Recently uploaded").click()
    await asyncio.sleep(1)
    device.shell("input swipe 241 474 241 374 1000")
    ui(resourceId=ui_vid).click()


for hash in hash_tags:
    asyncio.run(in_search(hash))
    asyncio.run(book_loop())


# asyncio.run(in_search("fyp"))
