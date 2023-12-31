import asyncio
from ppadb.client import Client as AdbClient
import os
import shutil
import json


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()


if len(devices) == 0:
    print("No devices")
    quit(0)


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]


def split_list(alist, wanted_parts):
    length = len(alist)
    return [
        alist[i * length // wanted_parts : (i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


async def open_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    # await asyncio.sleep(2)


async def verify_load_app(device):
    for device in devices:
        while True:
            try:
                await open_app(device)
                output = await get_output(device)
                if "MainPageFragment" in output:
                    print("App Loaded")
                    await asyncio.sleep(1)
                    break
            except Exception as error:
                pass
                print(error)


width = 480


def pixel(x, y, device):
    device.shell("screencap /sdcard/screencap.txt")
    device.pull(
        "/sdcard/screencap.txt",
        "./screen.temp",
    )
    with open("./screen.temp", "rb") as f:
        byte = f.read()[12:]
        pixel = (width * y + x) * 4
        return (byte[pixel], byte[pixel + 1], byte[pixel + 2])


new_videos = []
with open("new_videos.txt", "r", encoding="utf-8") as f:
    new_videos = f.read().splitlines()
new_users = []
with open("new_users.txt", "r", encoding="utf-8") as f:
    new_users = f.read().splitlines()

new_videos = split_list(new_videos, len(devices))


async def start_apps():
    for device in devices:
        await verify_load_app(device)


async def loop_vids(index, videos_chunk):
    for i, vid in enumerate(videos_chunk):
        print(f"{index} : ({i}/{len(videos_chunk)})")
        devices[index].shell(
            f"am start -W -a android.intent.action.VIEW -d {vid} {app_name}"
        )

        # if pixel(440, 290, devices[index]) == (255, 255, 255):
        #     print("not bookmarked yet")
        # else:
        #     print("bookamrkd allready")

        await asyncio.sleep(2)
        devices[index].shell(f"input keyevent 62")
        # await asyncio.sleep(1)
        # devices[index].shell(f"input tap 443 347")
        # await asyncio.sleep(1)
        # devices[index].shell(f"input tap 60 435")
        await asyncio.sleep(1)
        devices[index].shell(f"input tap 440 290")
        await asyncio.sleep(1)

    # devices[index].shell(f"am force-stop {app_name}")


async def main():
    await start_apps()
    await asyncio.gather(
        *[
            loop_vids(index, videos_chunk)
            for index, videos_chunk in enumerate(new_videos)
        ]
    )
    for device in devices:
        device.shell(f"am force-stop {app_name}")

    with open("used_users.txt", "a") as f:
        f.write("\n".join(new_users))


asyncio.run(main())
