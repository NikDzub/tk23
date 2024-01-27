import uiautomator2 as u2

# https://github.com/openatx/uiautomator2


def test():
    d = u2.connect("127.0.0.1:6555")
    running = d.app_list_running()
    print(running)
    screen = d.info.get("screenOn")
    print(screen)
    # inf = d.app_info("com.zhiliaoapp.musically")
    # print(inf)


if __name__ == "__main__":
    test()
