from uiautomator import device

bookmark_id = "com.zhiliaoapp.musically:id/d9x"
bookmark = device(resourceId=bookmark_id, selected="false", instance=0)

while True:
    print("h")
    if bookmark.wait.exists(timeout=3000):
        bookmark.click()
