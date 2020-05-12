import win32con
import win32gui
import wx

from .common import App, thread_safe


class DisplayPanel(wx.Frame):
    def __init__(self, app=App.instance(), parent=None, point_size=23, *args, **kw):
        super().__init__(parent, style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP | wx.BORDER_NONE | wx.CLIP_CHILDREN, *args,
                         **kw)

        self.app = app

        # let the frame can be clicked through, which means it won't block mouse events
        # http://wxwidgets.10942.n7.nabble.com/wxPython-and-pywin32-Implementing-on-top-transparency-and-click-through-on-Windows-tp30543.html
        hwnd = self.GetHandle()
        extended_style_settings = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               extended_style_settings | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

        # prevent text flickering
        self.SetDoubleBuffered(True)

        self.SetTransparent(200)
        self.SetBackgroundColour('black')

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.text = wx.StaticText(self)
        self.text.SetForegroundColour('white')

        font = self.text.GetFont()
        font.PointSize = point_size
        self.text.SetFont(font)

        sizer.Add(self.text, 0, wx.LEFT | wx.RIGHT, border=5)

    @thread_safe
    def display(self, text: str):
        # freeze/thaw also to prevent text flickering
        self.text.Freeze()
        self.text.SetLabelText(text)
        self.text.Thaw()

        self.GetSizer().Fit(self)
