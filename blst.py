#!/usr/bin/env python3


import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import random
from uiautomator import device
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(0)


bookmark_id = "com.zhiliaoapp.musically:id/d9x"
bookmark = device(resourceId=bookmark_id, selected="false", instance=0)


context_dir = "contexts/firefox_01"
context_dir = os.path.join(os.getcwd(), context_dir)
try:
    shutil.rmtree(f"{context_dir}/sessionstore-backups")
    os.remove(f"{context_dir}/sessionCheckpoints.json")
    os.remove(f"{context_dir}/sessionstore.jsonlz4")
except Exception as error:
    pass
    # print(error)

famouse_users = []
with open("famouse_users.txt", "r", encoding="utf-8") as f:
    famouse_users = f.read().splitlines()

used_users = []
with open("used_users.txt", "r", encoding="utf-8") as f:
    used_users = f.read().splitlines()


new_users = []
new_videos = []


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]


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


async def filter_response(response):
    global new_users
    global used_users

    if "/api/user/list/?" in response.url:
        try:
            response = await response.json()
            users = response["userList"]
            for user in users:
                if (
                    user["user"]["privateAccount"] == False
                    and user["stats"]["diggCount"] > 1
                    and user["stats"]["heartCount"] > 1
                    and user["stats"]["videoCount"] > 2
                    and user["user"]["uniqueId"] not in new_users
                    and user["user"]["uniqueId"] not in used_users
                ):
                    new_users.append(user["user"]["uniqueId"])
        except:
            pass


async def start_apps():
    for device in devices:
        await verify_load_app(device)


async def p1():
    await start_apps()

    async with async_playwright() as p:
        global new_users

        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        pg = context.pages[0]
        await pg.close()

        context.on("response", filter_response)

        for x in range(1):
            await context.new_page()

        async def get_users(page):
            global new_users
            await page.goto(
                f"https://www.tiktok.com/@{random.choice(famouse_users)}",
                wait_until="load",
            )
            await page.wait_for_timeout(104355400)
            await page.click('span[data-e2e="followers"]')

            while len(new_users) < 200:
                followers = await page.query_selector_all('p[class*="UniqueId"]')
                try:
                    await followers[len(followers) - 1].scroll_into_view_if_needed()
                except Exception as error:
                    pass
                    # print(error)

        await asyncio.gather(
            *[get_users(page) for index, page in enumerate(context.pages)]
        )

        async def get_vids(page, index):
            global new_users
            global used_users
            for user in new_users:
                try:
                    await page.goto(f"https://tiktok.com/@{user}")

                    await page.wait_for_selector(
                        f"a[href*='{user}/video']", timeout=5000
                    )

                    videos_selector = await page.query_selector_all(
                        f"a[href*='{user}/video']"
                    )

                    video_01 = videos_selector[0]
                    url_01 = await video_01.get_attribute("href")

                    used_users.append(user)

                    devices[index].shell(
                        f"am start -W -a android.intent.action.VIEW -d {url_01} {app_name}"
                    )
                    await asyncio.wait(2000)
                    # devices[index].shell(f"input keyevent 62")
                    if bookmark.wait.exists(timeout=2000):
                        bookmark.click()
                        print("saved video")
                    else:
                        print("not saved video")

                except Exception as error:
                    pass
                    # print(error)

        await asyncio.gather(
            *[get_vids(page, index) for index, page in enumerate(context.pages)]
        )

        with open("used_users.txt", "a") as f:
            f.write("\n".join(used_users))

        await context.close()


asyncio.run(p1())
