#!/usr/bin/env python3

# comment_on_emulator
# comment on vids from new_videos.txt
# comments from comments.txt

import asyncio
import uiautomator2 as u2
from ppadb.client import Client as AdbClient


client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()


new_vids_txt = []
comments_txt = []
app_name = "com.zhiliaoapp.musically"
pause = "com.zhiliaoapp.musically:id/f5t"
comments = "com.zhiliaoapp.musically:id/bpp"
add_comment = "com.zhiliaoapp.musically:id/bpu"
send_comment = "com.zhiliaoapp.musically:id/brj"

with open("new_videos.txt", "r") as file:
    lines = file.readlines()
    if len(lines) == 0:
        print("new_videos.txt is empty")
        exit(1)
    for line in lines:
        new_vids_txt.append(line.replace("\n", ""))
with open("comments.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        comments_txt.append(line.replace("\n", ""))


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
            print(vid)

            for comment in comments_txt:
                sess(resourceId=add_comment).click(10)
                sess(resourceId=add_comment).set_text(comment)
                sess(resourceId=send_comment).click(10)
                print(f"{client.serial} > {comment}")

        sess.shell(f"am force-stop {app_name}")
    except Exception as error:
        sess.shell(f"am force-stop {app_name}")
        print(error)
        pass


for client in devices:
    main(client)
