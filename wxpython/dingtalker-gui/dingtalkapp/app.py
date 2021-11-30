import wx, gui

import wxpythoner
import dingtalker


class AppFrame(gui.BaseMainFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.dingTalkClients.Set(dingtalker.getClientNames())
        self.dingTalkClients.SetSelection(0)

    def sendDingMessage(self, event):
        clientName = self.dingTalkClients.StringSelection
        markdownText = str(self.messageText.Value).strip()
        if not markdownText:
            wx.MessageBox("请填写要发送的消息内容！", parent=self)
        if clientName and markdownText:
            self.statusBar.StatusText = f"机器人[{clientName}]正在发送消息..."
            dingtalker.sendMarkdown(clientName,"你有一条消息", markdownText, atAll=True)
            self.statusBar.StatusText = f"机器人[{clientName}]发生消息成功！"

def main():
    wxpythoner.startApp(AppFrame)

if __name__ == '__main__':
    main()
