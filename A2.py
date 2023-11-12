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


xy_followers = "360 270"
# /////////////////////////////////////////////////

fin = False
swipe = "input swipe 120 500 100 400"
xy_first_user = "350 170"
xy_profile_f_video = "90 630"
xy_back = "30 70"
xy_bookmark = "690 1000"

for i in range(10):
    # /////////////////////////////////////////////////

    in_follower_profile = False

    while in_follower_profile == False:
        time.sleep(1)
        output_txt = device.shell(all_layers)
        index = output_txt.rindex("Added Fragments:")
        output_txt = output_txt[index:]
        index_end = output_txt.rindex("}")
        output_txt = output_txt[:index_end]

        if "UserProfile" in output_txt:
            in_follower_profile = True
            time.sleep(1)
            # print("In Follower Profile")

            def check_if_vid():
                width = 720

                def pixel(x, y):
                    device.shell("screencap /sdcard/screencap.txt")
                    device.pull(
                        "/sdcard/screencap.txt",
                        "./screen.temp",
                    )
                    with open("./screen.temp", "rb") as f:
                        byte = f.read()[12:]
                        pixel = (width * y + x) * 4
                        return (byte[pixel], byte[pixel + 1], byte[pixel + 2])

                if pixel(90, 630) == (255, 255, 255):
                    print("No Videos")
                    device.shell(f"input tap {xy_back}")

                else:
                    # print("Video Exists")
                    device.shell(f"input tap {xy_profile_f_video}")

                    in_video = False
                    while in_video == False:
                        time.sleep(1)
                        output_txt = device.shell(all_layers)
                        index = output_txt.rindex("Added Fragments:")
                        output_txt = output_txt[index:]
                        index_end = output_txt.rindex("}")
                        output_txt = output_txt[:index_end]

                        if "DetailFragment" in output_txt:
                            # print("in video")
                            in_video = True
                            device.shell(f"input tap {xy_bookmark}")
                            print("Bookmark")
                            time.sleep(1)
                            device.shell(f"input tap {xy_back}")

                        else:
                            device.shell(f"input tap {xy_profile_f_video}")

                    device.shell(f"input tap {xy_back}")

            check_if_vid()

        else:
            time.sleep(1)
            device.shell(swipe)
            device.shell(f"input tap {xy_first_user}")

        output_file = open("./out.txt", "w")
        output_file.write(output_txt)
        output_file.close()

device.shell("am force-stop com.zhiliaoapp.musically")
exit(0)
