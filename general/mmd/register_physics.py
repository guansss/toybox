import time

from utils import keyboard

FRAME_FIRST = 0

FRAME_FINAL = 9999

FRAME_SHIFT_KEY = 'right' if FRAME_FIRST <= FRAME_FINAL else 'left'


def main():
    for countdown in range(3, -1, -1):
        print(f'Waiting: {countdown}')
        time.sleep(1)

    frame_range = range(min(FRAME_FIRST, FRAME_FINAL), max(FRAME_FIRST, FRAME_FINAL) + 1)

    total = len(frame_range)

    if FRAME_SHIFT_KEY == 'left':
        frame_range = reversed(frame_range)

    for i, frame in enumerate(frame_range):
        print(f'Frame: {frame} ({i + 1}/{total})')

        # MMD does not respond to an instant press(), so we hold() instead
        keyboard.hold('enter')

        # go to next frame
        keyboard.hold(FRAME_SHIFT_KEY)

        time.sleep(0.2)


if __name__ == '__main__':
    main()
