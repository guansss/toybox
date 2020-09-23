import threading
import time

from gui_wx.panel import DisplayPanel
from utils import mouse

panel = DisplayPanel()
panel.Show()


def run():
    while 1:
        time.sleep(0.2)

        pos = mouse.pos()
        panel.display(", ".join(map(str, pos)))


thread = threading.Thread(target=run)
thread.setDaemon(True)
thread.start()

panel.app.MainLoop()
