#!/usr/bin/env python3

# python3 m1.py && python3 m2.py ||

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

famouse_users = []
with open("famouse_users.txt", "r", encoding="utf-8") as f:
    famouse_users = f.read().splitlines()

used_users = []
with open("used_users.txt", "r", encoding="utf-8") as f:
    used_users = f.read().splitlines()

new_users = []


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


# //////////
async def m1():
    async with async_playwright() as p:
        global new_users
        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        pg = context.pages[0]
        await pg.close()
        for x in range(1):
            await context.new_page()
        context.on("response", filter_response)

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

        with open("new_users.txt", "w") as f:
            f.write("\n".join(new_users))

        print(f"new users : {len(new_users)}")
        await context.close()


asyncio.run(m1())
