#!/usr/bin/env python3
# scrape_new_videos

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random


fam_users_json = open("users_videos.json")
fam_users = json.load(fam_users_json)
new_vids = []

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
            user_data_dir=context_dir, headless=True
        )
        # context.route("**/*", block_media)
        page = context.pages[0]
        await page.goto(
            "https://www.tiktok.com",
            wait_until="load",
        )

        length = len(fam_users["users"])
        for index, user in enumerate(fam_users["users"]):
            try:
                print(f"[{index}/{length}] {user}")
                await page.goto(f"https://www.tiktok.com/@{user}", wait_until="load")

                # print("timeout")
                # await page.wait_for_timeout(345435345)

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
                        new_vids.append(href)
                        print(f"{href}")
                    else:
                        # print(f"{href} allready exists")
                        pass
            except:
                pass

        with open("users_videos.json", "w") as outfile:
            json.dump(fam_users, outfile)
        with open("new_videos.txt", "w") as outfile:
            for index, row in enumerate(new_vids):
                if index < 2:
                    outfile.write(str(row) + "\n")
        await context.close()


asyncio.run(p1())
