from uiautomator import device
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

adb_client_device = devices[0]


new_videos = []
with open("new_videos.txt", "r", encoding="utf-8") as f:
    new_videos = f.read().splitlines()


def split_list(alist, wanted_parts):
    length = len(alist)
    return [
        alist[i * length // wanted_parts : (i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


new_videos = split_list(new_videos, len(devices))


bookmark_id = "com.zhiliaoapp.musically:id/d9x"
bookmark = device(resourceId=bookmark_id, selected="false", instance=0)


async def loop_vids(index, videos_chunk):
    for i, vid in enumerate(videos_chunk):
        print(f"{index} : ({i}/{len(videos_chunk)})")
        print(vid)
        devices[index].shell(
            f"am start -W -a android.intent.action.VIEW -d {vid} {app_name}"
        )
        if bookmark.wait.exists(timeout=3000):
            bookmark.click()


async def main():
    await asyncio.gather(
        *[
            loop_vids(index, videos_chunk)
            for index, videos_chunk in enumerate(new_videos)
        ]
    )
    for device in devices:
        device.shell(f"am force-stop {app_name}")


asyncio.run(main())
