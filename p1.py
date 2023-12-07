#!/usr/bin/env python3

# python3 p1.py && python3 p2.py ||

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random

context_dir = "contexts/firefox_01"
context_dir = os.path.join(os.getcwd(), context_dir)
try:
    shutil.rmtree(f"{context_dir}/sessionstore-backups")
    os.remove(f"{context_dir}/sessionCheckpoints.json")
    os.remove(f"{context_dir}/sessionstore.jsonlz4")
except Exception as error:
    pass
    # print(error)

# BLOCK_RESOURCE_TYPES = [
#     "beacon",
#     "csp_report",
#     "font",
#     "image",
#     "imageset",
#     "media",
#     "object",
#     "texttrack",
#     "stylesheet",
# ]
# BLOCK_RESOURCE_NAMES = [
#     "adzerk",
#     "analytics",
#     "cdn.api.twitter",
#     "doubleclick",
#     "exelator",
#     "facebook",
#     "fontawesome",
#     "google",
#     "google-analytics",
#     "googletagmanager",
# ]
# async def intercept_route(route):
#     if route.request.resource_type in BLOCK_RESOURCE_TYPES:
#         return await route.abort()
#     if any(key in route.request.url for key in BLOCK_RESOURCE_NAMES):
#         return await route.abort()
#     return route.continue_()


famouse_users = []
with open("famouse_users.txt", "r", encoding="utf-8") as f:
    famouse_users = f.read().splitlines()

used_users = []
with open("used_users.txt", "r", encoding="utf-8") as f:
    used_users = f.read().splitlines()


new_users = []
new_videos = []


async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


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


async def p1():
    async with async_playwright() as p:
        global new_users

        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        # context.route("**/*", block_media)
        pg = context.pages[0]
        await pg.wait_for_timeout(435435345)
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
            await page.wait_for_timeout(1000)
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

        def split_list(list, parts):
            length = len(list)
            return [
                list[i * length // parts : (i + 1) * length // parts]
                for i in range(parts)
            ]

        with open("new_users.txt", "w") as f:
            f.write("\n".join(new_users))
        new_users = split_list(new_users, len(context.pages))

        async def get_vids(page, index):
            global new_users
            for user in new_users[index]:
                try:
                    await page.goto(f"https://tiktok.com/@{user}")
                    # await page.wait_for_timeout(276000)

                    await page.wait_for_selector(
                        f"a[href*='{user}/video']", timeout=5000
                    )

                    videos_selector = await page.query_selector_all(
                        f"a[href*='{user}/video']"
                    )

                    # for video in videos_selector:
                    #     url = await video.get_attribute("href")
                    #     new_videos.append(url)

                    video_01 = videos_selector[0]
                    url_01 = await video_01.get_attribute("href")

                    # video_random = random.choice(videos_selector)
                    # url_random = await video_random.get_attribute("href")

                    new_videos.append(url_01)
                    print(url_01)

                except Exception as error:
                    pass
                    # print(error)

        await asyncio.gather(
            *[get_vids(page, index) for index, page in enumerate(context.pages)]
        )

        with open("new_videos.txt", "w") as f:
            f.write("\n".join(new_videos))

        # print(new_users)
        # print(new_videos)
        await context.close()


asyncio.run(p1())
