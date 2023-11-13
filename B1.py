#!/usr/bin/env python3

from ppadb.client import Client as AdbClient
import time
import asyncio

client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

if len(devices) == 0:
    print("No devices")
    quit(0)

app_name = "com.zhiliaoapp.musically"
run = True


async def search_for(device, index, username):
    if device.layer == "main":
        print("on main we can search")

    else:
        print("not on main how 2 srarch?")


# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴


async def check_loaded(device):
    cur_layer = None

    print(device.index)

    # def trnslte_frgmnt(frgmnts):
    #     if "MainPageFragment" in frgmnts:
    #         cur_layer = "on main"
    #     elif "LiveRoomFragment" in frgmnts:
    #         cur_layer = "on live"
    #     elif "UserProfileFragment" in frgmnts:
    #         cur_layer = "on profile"
    #     elif "FollowRelationTabFragment" in frgmnts:
    #         cur_layer = "on followers"
    #     elif "DetailFragment" in frgmnts:
    #         cur_layer = "on video"
    #     elif "SearchResultFragmentNew" in frgmnts:
    #         cur_layer = "on SearchResultFragmentNew"
    #     else:
    #         print("wtf")

    # while cur_layer != "on main":
    #     try:
    #         dumpsys_act = f"dumpsys activity {app_name}"
    #         await asyncio.sleep(1)

    #         output = device[index].shell(dumpsys_act)
    #         index_start = output.rindex("Added Fragments:")
    #         index_end = output.rindex("}")

    #         frgmnts = frgmnts[index_start:index_end]

    #         cur_layer = trnslte_frgmnt(frgmnts)
    #         print(cur_layer)

    #     except Exception as error:
    #         print(error)


# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴


async def open_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    await asyncio.sleep(2)
    print(device.index)


# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴
# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴
# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴


async def initialize():
    for index, device in enumerate(devices):
        device.index = index
        device.errors = 0

        print(f"device.index :{device.index}")
        print(f"device.errors :{device.errors}")
        print("---")


async def main():
    await initialize()

    for device in devices:
        await open_app(device)

    await asyncio.gather(*[check_loaded(device) for device in enumerate(devices)])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
