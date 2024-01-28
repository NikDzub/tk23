import os  # proxy bypass in mac setting: *.local, 169.254/16
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

user_agent_rotator = UserAgent(
    software_names=software_names, operating_systems=operating_systems, limit=100
)




  

# ▶️
async def main():
    rand_user_agent = user_agent_rotator.get_random_user_agent()

    async with async_playwright() as p:

        browser = await p.chromium.launch(
                headless=False
            )
        page = await browser.new_page(user_agent=rand_user_agent)
        await stealth_async(page)
            
        await page.goto("https://www.tiktok.com")
        await page.wait_for_timeout(30000)
        await browser.contexts[0].storage_state(path=f"./allStates/newEmails4Reddit/blast_k1.json")
        print(f"✅")

        await browser.close()

            


asyncio.run(main())
