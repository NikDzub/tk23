#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient


client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


new_vids_txt = []
comments_txt = []
app_name = "com.zhiliaoapp.musically"
comments = "com.zhiliaoapp.musically:id/bpp"
add_comment = "com.zhiliaoapp.musically:id/bpu"
send_comment = "com.zhiliaoapp.musically:id/brj"

with open("new_vids.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        new_vids_txt.append(line.replace("\n", ""))
with open("comments.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        comments_txt.append(line.replace("\n", ""))


async def main(client):
    d = u2.connect(client.serial)
    sess = d.session(app_name, attach=True)

    for vid in new_vids_txt:
        sess.open_url(vid)
        sess(resourceId=comments).click(10)

        for comment in comments_txt:
            sess(resourceId=add_comment).click(10)
            sess(resourceId=add_comment).set_text(comment)
            sess(resourceId=send_comment).click(10)

    sess.shell(f"am force-stop {app_name}")


async def fu():
    await asyncio.gather(*[main(client) for index, client in enumerate(devices)])


asyncio.run(fu())
