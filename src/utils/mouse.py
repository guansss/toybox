import pyautogui


def pos():
    return pyautogui.position()


def click(x, y):
    pyautogui.click(x, y)


def press(key):
    pyautogui.press(key)
