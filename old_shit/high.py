#!/usr/bin/env python3
import asyncio
import uiautomator2 as u2

# uiautomatorviewer

app_name = "com.zhiliaoapp.musically"
comments = "com.zhiliaoapp.musically:id/bpp"
add_comment = "com.zhiliaoapp.musically:id/bpu"
send_comment = "com.zhiliaoapp.musically:id/brj"

new_vids_txt = []
with open("new_vids.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        new_vids_txt.append(line.replace("\n", ""))

comments_txt = []
with open("comments.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        comments_txt.append(line.replace("\n", ""))

d = u2.connect("127.0.0.1:6555")


async def main():
    sess = d.session(app_name, attach=True)

    for vid in new_vids_txt:
        sess.open_url(vid)
        sess(resourceId=comments).click(10)

        for comment in comments_txt:
            sess(resourceId=add_comment).click(10)
            sess(resourceId=add_comment).set_text(comment)
            sess(resourceId=send_comment).click(10)

    sess.shell(f"am force-stop {app_name}")


asyncio.run(main())
