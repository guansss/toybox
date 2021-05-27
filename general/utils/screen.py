from ctypes import windll

dc = windll.user32.GetDC(0)


# https://stackoverflow.com/a/62623486
def get_pixel(x: int, y: int):
    return tuple(int.to_bytes(windll.gdi32.GetPixel(dc, x, y), 3, "little"))
