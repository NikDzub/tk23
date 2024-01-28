import asyncio
from ppadb.client import Client as AdbClient
import os
import shutil
import json

# UserProfileFragment
# DetailFragment

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


new_users = []
new_users_copy = []
with open("new_users.txt", "r", encoding="utf-8") as f:
    new_users = f.read().splitlines()
new_users_copy = new_users
new_users = split_list(new_users, len(devices))


async def start_apps():
    for device in devices:
        await verify_load_app(device)


async def loop_users(index, users_chunk):
    for i, user in enumerate(users_chunk):
        try:
            print(f"device #{index} : {user} ({i}/{len(users_chunk)})")
            devices[index].shell(
                f"am start -W -a android.intent.action.VIEW -d https://www.tiktok.com/@{user} {app_name}"
            )
            await asyncio.sleep(10)
            devices[index].shell(f"am force-stop {app_name}")
            await asyncio.sleep(3)

            # while "UserProfileFragment" in await get_output(devices[index]):
            #     devices[index].shell(f"input swipe 200 400 300 100 40")
            #     await asyncio.sleep(1)
            #     devices[index].shell(f"input tap 100 350")
            #     await asyncio.sleep(2)
            #     devices[index].shell(f"input keyevent 62")
            #     await asyncio.sleep(1)
            #     devices[index].shell(f"input tap 440 290")
            #     await asyncio.sleep(1)
            #     break
        except:
            pass


async def main():
    # await start_apps()
    await asyncio.gather(
        *[loop_users(index, users_chunk) for index, users_chunk in enumerate(new_users)]
    )

    with open("used_users.txt", "a") as f:
        f.write("\n".join(new_users_copy))

    for device in devices:
        device.shell(f"am force-stop {app_name}")


asyncio.run(main())
