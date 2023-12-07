#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import random
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(0)


context_dir = "contexts/firefox_01"
context_dir = os.path.join(os.getcwd(), context_dir)
try:
    shutil.rmtree(f"{context_dir}/sessionstore-backups")
    os.remove(f"{context_dir}/sessionCheckpoints.json")
    os.remove(f"{context_dir}/sessionstore.jsonlz4")
except Exception as error:
    pass

famouse_users = []
with open("famouse_users.txt", "r", encoding="utf-8") as f:
    famouse_users = f.read().splitlines()


new_users = []
new_videos = []


async def filter_response(response):
    global new_users

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
                ):
                    new_users.append(user["user"]["uniqueId"])
        except:
            pass


def split_list(alist, wanted_parts):
    length = len(alist)
    return [
        alist[i * length // wanted_parts : (i + 1) * length // wanted_parts]
        for i in range(wanted_parts)
    ]


async def p1():
    async with async_playwright() as p:
        global new_users

        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        pg = context.pages[0]
        await pg.close()

        context.on("response", filter_response)

        for index, x in enumerate(devices):
            await context.new_page()
            devices[index].shell(
                f"am start -W -a android.intent.action.VIEW -d https://www.tiktok.com/@coinitiktok {app_name}"
            )

        async def get_users(page):
            global new_users
            random_user = random.choice(famouse_users)
            famouse_users.pop(famouse_users.index(random_user))
            await page.goto(
                f"https://www.tiktok.com/@{random_user}",
                wait_until="load",
            )
            await page.wait_for_timeout(1000)
            await page.click('span[data-e2e="followers"]')

            while len(new_users) < 50:
                followers = await page.query_selector_all('p[class*="UniqueId"]')
                try:
                    await followers[len(followers) - 1].scroll_into_view_if_needed()
                except Exception as error:
                    pass
                    # print(error)

        await asyncio.gather(
            *[get_users(page) for index, page in enumerate(context.pages)]
        )

        new_users = split_list(new_users, len(devices))

        async def get_vids(page, index):
            global new_users
            for user in new_users[index]:
                try:
                    await context.pages[index].goto(f"https://tiktok.com/@{user}")

                    await context.pages[index].wait_for_selector(
                        f"a[href*='{user}/video']", timeout=5000
                    )

                    videos_selector = await context.pages[index].query_selector_all(
                        f"a[href*='{user}/video']"
                    )

                    video_01 = videos_selector[0]
                    url_01 = await video_01.get_attribute("href")

                    devices[index].shell(
                        f"am start -W -a android.intent.action.VIEW -d {url_01} {app_name}"
                    )
                    await asyncio.wait(2000)
                    devices[index].shell(f"input keyevent 62")
                    devices[index].shell(
                        f"am start -W -a android.intent.action.VIEW -d https://www.tiktok.com/@coinitiktok {app_name}"
                    )

                except Exception as error:
                    pass

        await asyncio.gather(
            *[get_vids(page, index) for index, page in enumerate(context.pages)]
        )

        await context.close()


asyncio.run(p1())
