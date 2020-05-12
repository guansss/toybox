"""
Batch registers/unregisters OP bones in MMD.
"""

import threading
import time

from gui_wx.panel import DisplayPanel
from utils import mouse, keyboard

# ========================================= Configs ===============================================

# Make sure that you've selected the FRAME_FIRST in MMD before running this script!
FRAME_FIRST = 0
FRAME_FINAL = 1

OP_BUTTON = (337, 1357)

TARGET_BONE_DROPDOWN = (1204, 675)
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

    if SHIFT_KEY == 'left':
        frame_range = reversed(frame_range)

    for frame in frame_range:
        panel.display('Frame: %s' % frame)

        register_frame()

        # MMD does not respond to an instant press(), so we hold() instead
        keyboard.hold(SHIFT_KEY)

    panel.display('Finished')
    time.sleep(1)
    panel.Close()


def register_frame():
    mouse.click(*OP_BUTTON)

    # wait until the dialog has opened
    mouse.click(*TARGET_BONE_DROPDOWN, 0.3)
    mouse.click(*TARGET_BONE)

    mouse.click(*OP_MODEL_DROPDOWN)
    mouse.click(*OP_MODEL)

    if OP_BONE:
        mouse.click(*OP_BONE)

    mouse.click(*REGISTER_OP_BUTTON)
    mouse.click(*REGISTER_FRAME_BUTTON)

    mouse.click(*CLOSE_BUTTON)


if __name__ == '__main__':
    main()
