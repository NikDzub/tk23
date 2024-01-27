#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random


fam_users_json = open("famouse_users.json")
fam_users = json.load(fam_users_json)
new_vids = []

for user in fam_users["users"]:
    print(user)

context_dir = "contexts/firefox_01"
context_dir = os.path.join(os.getcwd(), context_dir)
try:
    shutil.rmtree(f"{context_dir}/sessionstore-backups")
    os.remove(f"{context_dir}/sessionCheckpoints.json")
    os.remove(f"{context_dir}/sessionstore.jsonlz4")
except Exception as error:
    pass
    # print(error)


async def p1():
    global fam_users
    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        # context.route("**/*", block_media)
        page = context.pages[0]
        await page.goto(
            "https://www.tiktok.com",
            wait_until="load",
        )

        for user in fam_users["users"]:
            try:
                await page.goto(f"https://www.tiktok.com/@{user}", wait_until="load")
                await page.wait_for_selector(
                    f"a[href*='https://www.tiktok.com/@{user}/video/']"
                )
                vids = await page.query_selector_all(
                    f"a[href*='https://www.tiktok.com/@{user}/video/']"
                )
                for vid in vids:
                    href = await vid.get_attribute("href")
                    if href not in fam_users["users"][user]:
                        fam_users["users"][user].append(href)
                        print(f"{href} - new video")
                        new_vids.append(href)
                    else:
                        # print(f"{href} allready exists")
                        pass
            except:
                pass

        with open("famouse_users.json", "w") as outfile:
            json.dump(fam_users, outfile)
        with open("new_vids.txt", "w") as outfile:
            for row in new_vids:
                outfile.write(str(row) + "\n")
        await context.close()


asyncio.run(p1())
