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


async def get_frgmnts(device, index):
    def trnslte_frgmnt(frgmnts):
        print(index)

        if "MainPageFragment" in frgmnts:
            # print("on main")
            device.layer = "main"

        # elif "CommentListPageFragment" in frgmnts:
        #     print("on comments")
        #     device.layer = "comments"

        elif "UserProfileFragment" in frgmnts:
            print("on profile")
            device.layer = "profile"

        elif "FollowRelationTabFragment" in frgmnts:
            print("on followers")
            device.layer = "followers"

        elif "DetailFragment" in frgmnts:
            print("on video")
            device.layer = "video"

        elif "SearchResultFragmentNew" in frgmnts:
            print("on SearchResultFragmentNew")
            device.layer = "search"

    while run:
        try:
            dumpsys_act = f"dumpsys activity {app_name}"
            await asyncio.sleep(1)

            frgmnts = device.shell(dumpsys_act)
            index_start = frgmnts.rindex("Added Fragments:")
            index_end = frgmnts.rindex("}")

            frgmnts = frgmnts[index_start:index_end]

            trnslte_frgmnt(frgmnts)
            device.layer = trnslte_frgmnt(frgmnts)

        except Exception as error:
            print(error)


# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴


async def open_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    await asyncio.sleep(2)
    await get_frgmnts(device)


# 🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴~🪴


async def strt():
    await asyncio.gather(
        *[get_frgmnts(device, index) for index, device in enumerate(devices)]
    )


async def main():
    await strt()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
