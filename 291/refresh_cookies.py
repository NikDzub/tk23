#!/usr/bin/env python3

# refresh cookies from cookies folder to the cookies_updated folder
# make sure the updated_cookies folder is empty

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


cookies_json = os.listdir("./cookies")


async def p1():
    for acc in cookies_json:
        print("---")
        print(acc)
        async with async_playwright() as p:
            context = await p.firefox.launch(headless=False)
            # context.route("**/*", block_media)
            page = await context.new_page(color_scheme="dark")
            await context.contexts[0].add_cookies(
                json.loads(Path(f"cookies/{acc}").read_text())
            )
            await page.goto(
                "https://www.tiktok.com/coin", wait_until="domcontentloaded"
            )

            try:
                await page.wait_for_selector(
                    'span[class*="SpanNameInfo"]', timeout=10000
                )
                cookies = await context.contexts[0].cookies()
                with open(f"cookies_updated/{acc}", "w") as outfile:
                    outfile.write(json.dumps(cookies))
                    print(f"new cookie - {acc}")

            except:
                print("error")
                pass

            await page.close()
            await context.close()


asyncio.run(p1())
