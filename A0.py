#!/usr/bin/env python3
from ppadb.client import Client as AdbClient
import time

client = AdbClient(host="127.0.0.1", port=5037)

devices = client.devices()
if len(devices) == 0:
    print("No devices")
    quit()
device = devices[0]

app_name = "com.zhiliaoapp.musically"
open_app = f"monkey -p {app_name} 1"

inside_app = False

device.shell(open_app)

output_txt = ""

while inside_app == False:
    # | grep '#1020030 android:id/navigationBarBackground'
    # | grep '#102002f android:id/statusBarBackground'
    all_layers = f"dumpsys activity {app_name}"

    output_txt = device.shell(all_layers)

    if "ProfilePageFragment" in output_txt:
        inside_app = True
        print("App Loaded")

    else:
        # print("not in app")
        time.sleep(1)

quit(1)
