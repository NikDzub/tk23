import os
import json
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


head = False

searcher = "./allStates/oneOnly/ihptto.json"


# handles
async def block_media(route, req):
    if req.resource_type in {"image", "media", "font", "stylesheet", "css"}:
        try:
            await route.abort()
        except:
            pass


# proxy = {
#     "server": "http://nproxy.site:10558",
#     "username": "aZ1nUR",
#     "password": "SYtmUSzaC8yF",
# }

random_users = []


async def main():
    async with async_playwright() as p:

        async def a_1():
            browser = await p.chromium.launch(
                headless=head,
                # proxy=proxy
            )
            page = await browser.new_page()
            await stealth_async(page)
            await browser.contexts[0].route("**/*", block_media)

            state_file = open(f"{searcher}")
            state_json = json.load(state_file)
            await browser.contexts[0].add_cookies(state_json["cookies"])

            # get into video
            await page.goto("https://www.tiktok.com/foryou", wait_until="load")
            await page.click("video")
            await page.wait_for_selector(
                'span[data-e2e="browse-like-icon"] svg', timeout=5000
            )
            await page.reload(wait_until="load")
            await page.wait_for_selector('div[class*="DivItemContainer"]')
            await page.click('div[class*="DivOtherInfo"]')

            # get into video

            jsScroll = open("./jsEvalScroll.js").read()

            await page.evaluate(jsScroll)
            await page.wait_for_timeout(10000)

            users = await page.query_selector_all('span[data-e2e="comment-username-1"]')

            for user in users:
                if random_users.__len__() > 5:
                    pass
                else:
                    try:
                        await user.hover()

                        async with page.expect_request(
                            "https://www.tiktok.com/api/user/detail/*",
                            timeout=10000,
                        ) as user_req:
                            user_val = await user_req.value
                            user_res = await user_val.response()
                            data = await user_res.json()
                            userInfo = data["userInfo"]

                            if (
                                userInfo["stats"]["followerCount"] < 6000
                                and userInfo["stats"]["videoCount"] > 10
                            ):
                                random_users.append(userInfo["user"]["id"])

                    except:
                        pass

            await page.close()
            await browser.close()

            with open("./randomUsers.json", "w") as outfile:
                json.dump(random_users, outfile)
                print(random_users)

        await a_1()


asyncio.run(main())
