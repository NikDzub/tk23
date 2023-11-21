#!/usr/bin/env python3

import asyncio
from ppadb.client import Client as AdbClient
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

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()

if len(devices) == 0:
    print("No devices")
    quit(0)


target_users = []
with open("target_users.txt", "r", encoding="utf-8") as f:
    target_users = f.read().splitlines()


def split_list(list, parts):
    length = len(list)
    return [list[i * length // parts : (i + 1) * length // parts] for i in range(parts)]


target_users = split_list(target_users, len(devices))
for index, chunk in enumerate(target_users):
    chunk.insert(0, devices[index])
# 0 index = device


async def get_output(device):
    await asyncio.sleep(1)
    output = device.shell(f"dumpsys activity {app_name}")
    index_start = output.rindex("Added Fragments:")
    index_end = output.rindex("}")
    return output[index_start:index_end]


async def start_app(device):
    open_app = f"monkey -p {app_name} 1"
    device.shell(open_app)
    # await asyncio.sleep(2)


async def verify_load_app(device):
    for device in devices:
        await start_app(device)
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


async def main():
    global target_users

    async with async_playwright() as p:
        context = await p.firefox.launch_persistent_context(
            user_data_dir=context_dir, headless=False
        )
        # page = await context.new_page()
        # sddfdfdfdfdfdfdfdf
        for chunk in target_users:
            await context.new_page()
        await context.pages[0].close()

        async def get_vids(users_chunk, page, index):
            for index, user in enumerate(users_chunk):
                if index != 0:
                    print(user)

                    await page.goto(
                        f"https://www.tiktok.com/@{user}", wait_until="load"
                    )
                    await page.wait_for_timeout(5000)

        for page in context.pages:
            await page.goto("https://www.tiktok.com", wait_until="load")
            await page.wait_for_timeout(356546)
            await asyncio.gather(
                *[
                    get_vids(users_chunk, page, index)
                    for index, users_chunk in enumerate(target_users)
                ]
            )
        print("done")
        await asyncio.sleep(456456)


asyncio.run(main())
