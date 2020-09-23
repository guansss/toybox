import time

import pyautogui


def press(key, delay=0.1):
    time.sleep(delay)
    pyautogui.press(key)


def hold(key, duration=0.01, delay=0.1):
    time.sleep(delay)

    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)
