#!/usr/bin/env python3


# python3 A0.py && python3 A1.py && python3 A2.py
# python3 A0.py && python3 A1.py && python3 A2.py &&
# python3 A0.py || python3 A1.py || python3 A2.py ||

from ppadb.client import Client as AdbClient
import time
import sys


client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit(1)
device = devices[1]

app_name = "com.zhiliaoapp.musically"
all_layers = f"dumpsys activity {app_name}"


xy_followers = "360 270"
# /////////////////////////////////////////////////

fin = False
swipe = "input swipe 120 500 100 400"
xy_first_user = "350 170"
xy_profile_f_video = "90 630"
xy_back = "30 70"


in_follower_profile = False

while in_follower_profile == False:
    time.sleep(1)
    output_txt = device.shell(all_layers)
    index = output_txt.rindex("Added Fragments:")
    output_txt = output_txt[index:]
    index_end = output_txt.rindex("}")
    output_txt = output_txt[:index_end]

    output_file = open("./out.txt", "w")
    print(output_txt)
    output_file.write(output_txt)
    output_file.close()


exit(0)
