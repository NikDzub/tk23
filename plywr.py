import asyncio
from playwright.async_api import async_playwright
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


async def main():
    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        page = context.pages[0]
        await page.goto("https://www.tiktok.com/@nickiminaj", wait_until="load")

        followers_selector = await page.query_selector("div")
        followers_selector.evaluate('e=>e.color = "red"')
        await page.click('span[data-e2e="followers"]')

        users_db = {"re50er500"}

        async def check_response(response):
            if "/api/user/list/?" in response.url:
                response = await response.json()
                users = response["userList"]
                for user in users:
                    if (user["stats"]["videoCount"]) != 0 or (
                        user["stats"]["diggCount"]
                    ) > 10:
                        users_db.add(user["user"]["uniqueId"])
                        print(users_db)

        page.on("response", check_response)

        while len(users_db) < 250:
            followers = await page.query_selector_all('p[class*="UniqueId"]')
            try:
                await followers[len(followers) - 1].scroll_into_view_if_needed()
            except:
                pass
        # com.amaze.filemanager
        # com.android.htmlviewer

        await page.wait_for_timeout(5435345)


asyncio.run(main())
