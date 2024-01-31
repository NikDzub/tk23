#!/usr/bin/env python3

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient


client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


new_vids_txt = []
app_name = "com.zhiliaoapp.musically"
pause = "com.zhiliaoapp.musically:id/f5t"
comments = "com.zhiliaoapp.musically:id/bpp"
actual_comment = "com.zhiliaoapp.musically:id/bzg"
add_comment = "com.zhiliaoapp.musically:id/bpu"
send_comment = "com.zhiliaoapp.musically:id/brj"

with open("new_videos.txt", "r") as file:
    lines = file.readlines()
    if len(lines) == 0:
        print("new_videos.txt is empty")
        exit(1)
    for line in lines:
        new_vids_txt.append(line.replace("\n", ""))


def main(client):
    try:
        d = u2.connect(client.serial)
        sess = d.session(app_name, attach=True)
        print("---")

        for vid in new_vids_txt:
            sess.open_url(vid)
            sess.app_wait(app_name, 20)

            sess(resourceId=comments).exists(timeout=20)
            sess(resourceId=pause).click(40)
            sess(resourceId=comments).click(40)

            comments_list = []
            for i in range(10):
                sess.swipe_ext("up", scale=0.8)
                for com in sess(resourceId=actual_comment):
                    if com.get_text() not in comments_list:
                        comments_list.append(com.get_text())
                        print(com.get_text())

            sess(resourceId="com.zhiliaoapp.musically:id/brjfakeee").exists(
                timeout=24350
            )

        sess.shell(f"am force-stop {app_name}")
    except Exception as error:
        sess.shell(f"am force-stop {app_name}")
        print(error)
        pass


for client in devices:
    main(client)
