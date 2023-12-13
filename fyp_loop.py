#!/usr/bin/env python3


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
ui_clear_search = "com.zhiliaoapp.musically:id/axp"
ui_pf_vid = "com.zhiliaoapp.musically:id/mwg"
ui_book_mark = "com.zhiliaoapp.musically:id/bsh"


hash_tags = ["fyp"]
# hash_tags = ["fyp", "fypシ", "viraltiktok"]
# ui.dump("hierarchy.xml")


def pixel(x, y, device):
    device.shell(f"screencap /sdcard/screencap{i}.txt")
    device.pull(
        f"/sdcard/screencap{i}.txt",
        f"./screen{i}.temp",
    )
    with open(f"./screen{i}.temp", "rb") as f:
        byte = f.read()[12:]
        pixel = (480 * y + x) * 4
        # print(byte[pixel], byte[pixel + 1], byte[pixel + 2])
        return (byte[pixel], byte[pixel + 1], byte[pixel + 2])


async def book_loop():
    already_saved = 0
    while already_saved < 10:
        try:
            device.shell("input swipe 10 149 10 0 100")
            await asyncio.sleep(0.5)
            device.shell(f"input keyevent 62")
            await asyncio.sleep(1)

            if pixel(447, 272, device) == (229, 229, 229):
                device.shell(f"input tap 447 272")
                await asyncio.sleep(1)
                # device.shell(f"input keyevent --longpress 22")
                # await asyncio.sleep(1)
                # device.shell(f"input keyevent --longpress 21")

                # # ui(resourceId=ui_book_mark).click()
                # ui(
                #     descriptionContains="Add or remove this video from Favorites"
                # ).click()
            else:
                already_saved = already_saved + 1
                print(already_saved)
                if already_saved == 10:
                    device.shell(f"am force-stop {app_name}")

            await asyncio.sleep(1)
        except:
            already_saved = already_saved + 1
            print(already_saved)
            if already_saved == 10:
                device.shell(f"am force-stop {app_name}")
                await asyncio.sleep(5)
            pass


async def go_search(hash_tag):
    device.shell(f"am force-stop {app_name}")
    await asyncio.sleep(5)

    device.shell(
        f"am start -W -a android.intent.action.VIEW -d https://www.tiktok.com/@coinitiktok {app_name}"
    )
    await asyncio.sleep(1)
    device.shell("input swipe 10 149 10 0 100")
    await asyncio.sleep(1)
    device.shell(f"input tap 100 292")
    await asyncio.sleep(1)

    # ui(resourceId=ui_pf_vid).click()
    # ui(textContains="Find related").click()

    for i in range(2):
        device.shell(f"input tap 200 75")
        await asyncio.sleep(1)

        # device.shell(f"input keyevent --longpress 22")
        device.shell(f"input keyevent --longpress 67 67 67 67 67 67 67 67 67 67")
        await asyncio.sleep(1)

        device.shell(f"input text '{hash_tag}'")
        device.shell(f"input keyevent 66")
        await asyncio.sleep(3)
    # for i in range(1):
    #     ui(resourceId=ui_search).click()
    #     await asyncio.sleep(1)
    #     device.shell(f"input keyevent 66")
    # ui(text="Recently uploaded").click()
    device.shell(f"input tap 435 207")

    # ui(text="Unwatched").click()
    await asyncio.sleep(1)
    device.shell("input swipe 241 474 241 374 1000")
    await asyncio.sleep(1)
    # ui(resourceId=ui_vid).click()
    device.shell(f"input tap 120 469")


while True:
    for hash in hash_tags:
        asyncio.run(go_search(hash))
        asyncio.run(book_loop())
