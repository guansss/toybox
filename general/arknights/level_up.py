import time
import winsound

from utils import mouse, screen

CARD_POS = (1200, 650)
CONFIRM_POS = (2160, 1340)
CONFIRM_BUTTON_COLOR = (0, 112, 161)
CONFIRM_BUTTON_COLOR_FOCUSED = (0, 117, 168)

total = 20


def run():
    time.sleep(3)
    i = 0

    while screen.get_pixel(*CONFIRM_POS) in [CONFIRM_BUTTON_COLOR, CONFIRM_BUTTON_COLOR_FOCUSED]:
        i += 1
        print(i)

        mouse.long_click(*CARD_POS, 2.5)
        mouse.click(*CONFIRM_POS)

        time.sleep(1)  # wait for the network

    winsound.Beep(1500, 100)
    winsound.Beep(1500, 100)


run()
