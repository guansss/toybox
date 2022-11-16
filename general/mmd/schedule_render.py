import datetime
import os
import sys
import time

sys.path.append(r'C:\Users\82114\PyProjects\toybox\general')

from utils import mouse, keyboard, screen

TIME = datetime.datetime.now()#.combine(datetime.date.today(), datetime.time(11))

RENDER_TIME_ANTICIPATION = datetime.time(1)

OK_BTN = (1225, 825)
EXIT_BTN = (2550, 10)
EXIT_BTN1 = (1330, 720)
EXIT_BTN2 = (1295, 600)
EXIT_BTN_COLOR = (255, 255, 255)

SCREENSHOT_DIR = ''


def main1():
    print('Started')
    while is_closable1():
        time.sleep(60)

    print('Closable')
    time.sleep(10)
    screen.capture(None, SCREENSHOT_DIR + 'closable.jpg')

    # if is_closable2():
    #     mouse.click(*EXIT_BTN1)

    time.sleep(30)
    mouse.click(*EXIT_BTN)
    time.sleep(30)

    screen.capture(None, SCREENSHOT_DIR + 'closed.jpg')

    time.sleep(10)

    if not is_closable():
        os.system('shutdown -s -t 0')


def main():
    # main1()
    # return
    
    print(f'Scheduled at {TIME}')

    delta = TIME - datetime.datetime.now()
    print(f'Rendering Will start after {delta} ({delta.total_seconds()}secs)')

    time.sleep(delta.total_seconds())

    # wake up the screen
    keyboard.press('shift')
    time.sleep(10)

    screen.capture(None, SCREENSHOT_DIR + 'ready.jpg')

    mouse.click(*OK_BTN)
    print('Started')
    time.sleep(60)

    screen.capture(None, SCREENSHOT_DIR + 'start.jpg')

    # wait until the rendering has finished
    while not is_closable():
        time.sleep(60)

    screen.capture(None, SCREENSHOT_DIR + 'closable.jpg')

    time.sleep(60)
    mouse.click(*EXIT_BTN)
    time.sleep(30)

    screen.capture(None, SCREENSHOT_DIR + 'closed.jpg')

    time.sleep(10)

    if not is_closable():
        os.system('shutdown -s -t 0')


def is_closable():
    return screen.get_pixel(*EXIT_BTN) == EXIT_BTN_COLOR


def is_closable1():
    return screen.get_pixel(*EXIT_BTN1) == EXIT_BTN_COLOR


def is_closable2():
    return screen.get_pixel(*EXIT_BTN2) == EXIT_BTN_COLOR


if __name__ == '__main__':
    main()
