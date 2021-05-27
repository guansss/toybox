import time

import pyautogui


def pos():
    return pyautogui.position()


def click(x: int, y: int):
    pyautogui.click(x, y)


def long_click(x: int, y: int, duration: float):
    pyautogui.mouseDown(x, y)
    time.sleep(duration)
    pyautogui.mouseUp()
