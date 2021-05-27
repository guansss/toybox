"""
Batch registers/unregisters OP bones in MMD.

Usage:

Set FRAME_FIRST and FRAME_FINAL respectively to the start and end of frames that you want to edit.
When FRAME_FIRST is greater than FRAME_FINAL, frame operations will be done from right to left.

You would also need to modify those mouse-clicking coordinates in configs, there's a script at
"misc/display_cursor_pos.py" to help with this.

Then run the script and remember to switch to the MMD window.
"""

import threading
import time

from gui_wx.panel import DisplayPanel
from utils import mouse, keyboard

# ========================================= Configs ===============================================

# Make sure that you've selected the FRAME_FIRST in MMD before running this script!
FRAME_FIRST = 2248
FRAME_FINAL = 2225

OP_BUTTON = (337, 1357)

TARGET_BONE_DROPDOWN = (1204, 635)
TARGET_BONE = (1183, 661)

OP_MODEL_DROPDOWN = (1209, 676)
OP_MODEL = (1195, 694)
OP_BONE = None

REGISTER_OP_BUTTON = (1280, 708)
REGISTER_FRAME_BUTTON = (1280, 828)

CLOSE_BUTTON = (1448, 572)

# =================================================================================================

SHIFT_KEY = 'right' if FRAME_FIRST <= FRAME_FINAL else 'left'


def main():
    panel = DisplayPanel()
    panel.Show()

    thread = threading.Thread(target=run, args=(panel,))
    thread.setDaemon(True)
    thread.start()

    panel.app.MainLoop()


def run(panel):
    for countdown in range(3, -1, -1):
        panel.display('Wait: %s' % str(countdown))
        time.sleep(1)

    frame_range = range(min(FRAME_FIRST, FRAME_FINAL), max(FRAME_FIRST, FRAME_FINAL) + 1)

    total = len(frame_range)

    if SHIFT_KEY == 'left':
        frame_range = reversed(frame_range)

    for i, frame in enumerate(frame_range):
        panel.display('Frame: %s (%s/%s)' % (frame, i + 1, total))

        register_frame()

        # MMD does not respond to an instant press(), so we hold() instead
        keyboard.hold(SHIFT_KEY)

    panel.display('Finished')
    time.sleep(1)
    panel.Close()


def register_frame():
    mouse_click(*OP_BUTTON)

    # wait until the dialog has opened
    mouse_click(*TARGET_BONE_DROPDOWN, 0.3)
    mouse_click(*TARGET_BONE)

    mouse_click(*OP_MODEL_DROPDOWN)
    mouse_click(*OP_MODEL)

    if OP_BONE:
        mouse_click(*OP_BONE)

    mouse_click(*REGISTER_OP_BUTTON)
    mouse_click(*REGISTER_FRAME_BUTTON)

    mouse_click(*CLOSE_BUTTON)


def mouse_click(x: int, y: int, delay: float = 0.1):
    time.sleep(delay)
    mouse.click(x, y)


if __name__ == '__main__':
    main()
