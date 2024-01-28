#!/usr/bin/env python3


import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random
from pathlib import Path


async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet"}:
        try:
            await route.abort()
        except:
            pass


accounts = []
with open("./etc/accs.txt") as f:
    f = list(f)
    for acc in f:
        accounts.append(acc.split(":"))


async def p1():
    for acc in accounts:
        async with async_playwright() as p:
            context = await p.firefox.launch(headless=False)
            # context.route("**/*", block_media)
            page = await context.new_page(color_scheme="dark")
            await page.goto(
                "https://www.tiktok.com/login/phone-or-email/email", wait_until="load"
            )
            await page.keyboard.press("Tab")
            await page.keyboard.type(acc[0])
            await page.keyboard.press("Tab")
            await page.keyboard.type(acc[1])
            await page.keyboard.press("Enter")

            try:
                await page.wait_for_url(
                    "https://www.tiktok.com/foryou?lang=en", timeout=30000
                )
                if page.url == "https://www.tiktok.com/foryou?lang=en":
                    cookies = await context.contexts[0].cookies()
                    with open(f"cookies/{acc[0]}.json", "w") as outfile:
                        outfile.write(json.dumps(cookies))
                    print(f"new cookie - {acc[0]}")
            except:
                print(f"error - {acc[0]}")
                pass

            await page.wait_for_timeout(1000)
            await page.close()
            await context.close()
            # await context.contexts[0].add_cookies(
            #     json.loads(Path("cookies/coinitiktok.json").read_text())
            # )
            # print("new cookie")
            # await page.wait_for_timeout(30053450)
            # await page.goto("https://www.tiktok.com", wait_until="load")
            # await page.wait_for_timeout(60000)


asyncio.run(p1())
