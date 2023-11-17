import asyncio
from playwright.async_api import async_playwright
import os
import shutil

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
        print(1)
        await page.goto("https://tiktok.com/")
        await page.wait_for_timeout(546546546)
        print(3)


asyncio.run(main())
