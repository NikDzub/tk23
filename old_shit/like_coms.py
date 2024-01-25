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
            user_data_dir=context_dir,
            headless=False,
            # user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.3",
            # is_mobile=True,
            # viewport={"width": 400, "height": 800},
        )
        # context.route("**/*", block_media)
        page = context.pages[0]
        await page.goto("https://www.tiktok.com/@charlidamelio", wait_until="load")
        first_vid = await page.wait_for_selector("video")
        await first_vid.click()
        await page.wait_for_selector('span[data-e2e="comment-like-count"]')

        while True:
            whites = await page.query_selector_all()

        await page.wait_for_timeout(435435345)
        await page.close()

        context.on("response", filter_response)


asyncio.run(p1())
