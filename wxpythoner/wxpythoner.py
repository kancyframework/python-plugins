import wx


def startApp(frameClass, *args, **kwargs):
    """
    启动APP
    :param frameClass: 类型 或者 类名
    :param args: 参数
    :param kwargs: 关键字
    :return:
    """
    if isinstance(frameClass, str):
        import sys
        frameClass = getattr(sys.modules[__name__], frameClass)
    if issubclass(frameClass, wx.Frame):
        frameClass = frameClass
        app = wx.App()
        frame = frameClass(None, *args, **kwargs)
        frame.Show()
        app.MainLoop()
