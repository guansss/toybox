import time

import pyautogui


def pos():
    return pyautogui.position()


def click(x, y, delay=0.1):
    time.sleep(delay)
    pyautogui.click(x, y)
