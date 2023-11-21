import asyncio
from playwright.async_api import async_playwright
from ppadb.client import Client as AdbClient
import os
import shutil
import json


context_dir = "contexts/firefox_01"
context_dir = os.path.join(os.getcwd(), context_dir)

try:
    shutil.rmtree(f"{context_dir}/sessionstore-backups")
    os.remove(f"{context_dir}/sessionCheckpoints.json")
    os.remove(f"{context_dir}/sessionstore.jsonlz4")
except Exception as error:
    pass
    # print(error)


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


users_db = []


async def filter_response(response):
    global users_db
    if "/api/user/list/?" in response.url:
        response = await response.json()
        users = response["userList"]
        for user in users:
            if (
                (user["user"]["privateAccount"]) != "false"
                and (user["stats"]["videoCount"]) > 2
                and user["user"]["uniqueId"] not in users_db
            ):
                users_db.append(user["user"]["uniqueId"])


async def open_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    # await asyncio.sleep(2)


async def verify_load_app(device):
    for device in devices:
        await open_app(device)
        while True:
            try:
                output = await get_output(device)
                if "MainPageFragment" in output:
                    # print("App Loaded")
                    await asyncio.sleep(1)
                    break
            except Exception as error:
                pass
                # print(error)


async def main(device):
    global users_db

    await verify_load_app(device)

    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        page = context.pages[0]
        await page.goto("https://www.tiktok.com/@nickiminaj", wait_until="load")
        await page.wait_for_timeout(1000)

        await page.click('span[data-e2e="followers"]')
        page.on("response", filter_response)

        while len(users_db) < 150:
            followers = await page.query_selector_all('p[class*="UniqueId"]')
            try:
                await followers[len(followers) - 1].scroll_into_view_if_needed()
            except Exception as error:
                pass
                # print(error)

        users_db = users_db[10:]

        for user in users_db:
            videos_db = []

            async def book_mark(device, url):
                device.shell(
                    f"am start -W -a android.intent.action.VIEW -d {url} {app_name}"
                )
                await asyncio.sleep(2)
                device.shell(f"input tap 440 290")
                await asyncio.sleep(1)

            try:
                await page.goto(f"https://tiktok.com/@{user}", wait_until="load")
                await page.wait_for_selector(f"a[href*='{user}/video']")

                videos_selector = await page.query_selector_all(
                    f"a[href*='{user}/video']"
                )

                for video in videos_selector:
                    url = await video.get_attribute("href")
                    if url not in videos_db and len(videos_db) < 2:
                        videos_db.append(url)

                for url in videos_db:
                    await book_mark(device, url)

            except Exception as error:
                pass
                # print(error)


async def start_bot():
    asyncio.gather(*[main(device) for device in devices])


asyncio.run(start_bot())
