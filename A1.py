#!/usr/bin/env python3
from ppadb.client import Client as AdbClient
import time
import sys


client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(1)
device = devices[0]

app_name = "com.zhiliaoapp.musically"
all_layers = f"dumpsys activity {app_name}"

users = ["dhhyuniee", "vantoan___", "bellapoarch"]
search_usr = users[2]
print(f"Search user: {search_usr}")

xy_search = "690 75"
xy_profile = "300 200"
xy_followers = "360 270"
# /////////////////////////////////////////////////

in_search = False

while in_search == False:
    output_txt = device.shell(all_layers)
    index = output_txt.rindex("Added Fragments:")
    output_txt = output_txt[index:]
    index_end = output_txt.rindex("}")
    output_txt = output_txt[:index_end]

    if "SearchResult" in output_txt:
        in_search = True
        print("In search")
        device.shell(f"input text {search_usr}")
        time.sleep(1)
        device.shell(f"input keyevent 66")
        time.sleep(1)
        device.shell(f"input tap {xy_profile}")

    else:
        time.sleep(1)
        device.shell(f"input tap {xy_search}")

    output_file = open("./out.txt", "w")
    output_file.write(output_txt)
    output_file.close()

# /////////////////////////////////////////////////

in_profile = False

while in_profile == False:
    output_txt = device.shell(all_layers)
    index = output_txt.rindex("Added Fragments:")
    output_txt = output_txt[index:]
    index_end = output_txt.rindex("}")
    output_txt = output_txt[:index_end]

    if "UserProfile" in output_txt:
        in_profile = True
        print(f"In Profile :{search_usr}")
        time.sleep(1)
        device.shell(f"input tap {xy_followers}")

    else:
        time.sleep(1)
        device.shell(f"input tap {xy_profile}")

    output_file = open("./out.txt", "w")
    output_file.write(output_txt)
    output_file.close()

# /////////////////////////////////////////////////

in_follow = False

while in_follow == False:
    output_txt = device.shell(all_layers)
    index = output_txt.rindex("Added Fragments:")
    output_txt = output_txt[index:]
    index_end = output_txt.rindex("}")
    output_txt = output_txt[:index_end]

    if "FollowRelation" in output_txt:
        in_follow = True
        print(f"In Followers List")
        time.sleep(1)

    else:
        time.sleep(1)
        device.shell(f"input tap {xy_followers}")

    output_file = open("./out.txt", "w")
    output_file.write(output_txt)
    output_file.close()

exit(0)
