#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import os
import shutil
import json
import random
from datetime import datetime

username_list = []
with open("./username_list.txt") as f:
    for line in f.readlines():
        username_list.append(line.replace("\n", ""))
username_list_length = len(username_list)
random.shuffle(username_list)

used_vids = []
with open("used_videos.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        used_vids.append(line.replace("\n", ""))

url = "https://www.tiktok.com/"
vids_api = "https://www.tiktok.com/api/post/item_list/*"
new_vids = []


class Video:
    def __init__(
        self,
        creator,
        verified,
        vid_id,
        hr_ago,
        comments,
        likes,
        plays,
        bookmarks,
        shares,
    ):
        self.creator = creator
        self.verified = verified
        self.vid_id = vid_id
        self.hr_ago = hr_ago
        self.comments = comments
        self.likes = likes
        self.plays = plays
        self.bookmarks = bookmarks
        self.shares = shares

    def display_info(self):
        print(
            f"{url}@{self.creator}/video/{self.vid_id} \nhr_ago: {int(self.hr_ago)} comments: {self.comments} likes: {self.likes} plays: {self.plays} bookmarks: {self.bookmarks} shares: {self.shares}"
        )

    def video_url(self):
        # print(f"{url}@{self.creator}/video/{self.vid_id}")
        return f"{url}@{self.creator}/video/{self.vid_id}"


def split_list(lst, segments):
    segment_size = len(lst) // segments
    remainder = len(lst) % segments
    segments_list = []
    start = 0
    for i in range(segments):
        if i < remainder:
            end = start + segment_size + 1
        else:
            end = start + segment_size
        segments_list.append(lst[start:end])
        start = end
    return segments_list


username_list = split_list(username_list, 2)


async def p1(seg):
    global new_vids
    async with async_playwright() as p:
        context = await p.firefox.launch(headless=False)

        page = await context.new_page()

        await page.goto(
            url,
            wait_until="load",
        )

        for index, user in enumerate(seg):
            if len(new_vids) < 2:
                try:
                    print(f"{user}")
                    async with page.expect_request(vids_api, timeout=10000) as first:
                        await page.goto(f"{url}@{user}", timeout=10000)

                    first_request = await first.value
                    response = await first_request.response()
                    response_body = await response.body()
                    videos_json = json.loads(response_body)["itemList"]

                    current_timestamp = datetime.now().timestamp()

                    for vid in videos_json:
                        vid = Video(
                            vid["author"]["uniqueId"],
                            vid["author"]["verified"],
                            vid["id"],
                            ((current_timestamp - vid["createTime"]) / 3600),
                            vid["stats"]["commentCount"],
                            vid["stats"]["diggCount"],
                            vid["stats"]["playCount"],
                            vid["stats"]["collectCount"],
                            vid["stats"]["shareCount"],
                        )
                        used = vid.video_url() in used_vids
                        valid = (
                            (vid.likes / (vid.hr_ago * 1000) > 0.8)
                            and vid.hr_ago < 20
                            and used == False
                        )
                        if valid and len(new_vids) < 2:
                            new_vids.append(vid.video_url())
                            used_vids.append(vid.video_url())

                except Exception as error:
                    # print(error)
                    pass

        await page.close()
        await context.close()

        with open("new_videos.txt", "w") as outfile:
            for index, row in enumerate(new_vids):
                outfile.write(str(row) + "\n")
        with open("used_videos.txt", "w") as outfile:
            for index, row in enumerate(used_vids):
                outfile.write(str(row) + "\n")


async def ppp():
    await asyncio.gather(*[p1(seg) for index, seg in enumerate(username_list)])


asyncio.run(ppp())
