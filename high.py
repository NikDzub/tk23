import asyncio
from ppadb.client import Client as AdbClient
import uiautomator2 as u2

# uiautomatorviewer

import os
import shutil
import json

client = AdbClient(host="127.0.0.1", port=5037)
app_name = "com.zhiliaoapp.musically"
global devices
devices = client.devices()
d = u2.connect("127.0.0.1:6555")


async def main():
    like = d(resourceId="com.zhiliaoapp.musically:id/cia")
    print(like.info)


asyncio.run(main())
