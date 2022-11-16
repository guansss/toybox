from ctypes import windll

from PIL import ImageGrab

dc = windll.user32.GetDC(0)


# https://stackoverflow.com/a/62623486
def get_pixel(x: int, y: int):
    return tuple(int.to_bytes(windll.gdi32.GetPixel(dc, x, y), 3, "little"))


def capture(bbox: tuple = None, save_to: str = None):
    image = ImageGrab.grab(bbox)

    if save_to:
        image.save(save_to)

    return image
