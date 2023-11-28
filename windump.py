import asyncio
from ppadb.client import Client as AdbClient
import os
import shutil
import json
import xmltodict

o = xmltodict.parse("<e> <a>text</a> <a>text</a> </e>")
json.dumps(o)  # '{"e": {"a": ["text", "text"]}}'


client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(0)


async def win_dump(index, device):
    i = f"window_dump{index}"
    device.shell(f"uiautomator dump /sdcard/{i}.xml")
    device.pull(f"/sdcard/{i}.xml", f"./window_dump/{i}.xml")
    with open(f"./window_dump/{i}.xml", "r", encoding="utf-8") as f:
        xml_trash = f.read()
        json_parse = xmltodict.parse(xml_trash)
        win_dump = json.dumps(json_parse)
        print(win_dump)
        with open(f"./window_dump/{i}.json", "w") as f:
            f.write(win_dump)


async def main():
    await asyncio.gather(
        *[win_dump(index, device) for index, device in enumerate(devices)]
    )


asyncio.run(main())
