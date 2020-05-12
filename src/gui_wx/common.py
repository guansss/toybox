from typing import Callable

import wx

app = None


def thread_safe(func: Callable):
    def wrapper(self, *args, **kw):

        def runner():
            try:
                return func(self, *args, **kw)
            except Exception as e:
                # catch and ignore the error of "wrapped C/C++ object of type <...> has been deleted"
                if 'has been deleted' not in str(e):
                    raise

        # self will be False when the wx.Window instance has been destroyed
        if self:
            return wx.CallAfter(runner)

    return wrapper


class App(wx.App):
    def __init__(self):
        super().__init__()

    @staticmethod
    def instance():
        global app

        if not app:
            app = App()

        return app
