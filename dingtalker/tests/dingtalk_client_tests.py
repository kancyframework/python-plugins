from dingtalker import DingTalkClient

if __name__ == "__main__":
    accessToken = '1676877387c8a486a8c81491def78a931d0a7df65e3eff0c3ef28c4a25b5cc50'
    secret = 'SEC92e1603e992a14af2b27efdb6753bf08eadc694ee6dfc9cb458327899dbd2695'

    d = DingTalkClient(accessToken, secret, debug=True)
    d.sendMarkdownFile("标题","md/file.md", "18079637336", name="kancy", age=18)
    # d.sendText("大家都打了吗？", "18079637336")
    # d.sendMarkdown("标题","## 大家都打了吗？", "18079637336")
    # d.sendLink("好消息！好消息！","本群与百度成功达成合作关系，今后大家有什么不懂的可以直接百度搜索，不用再群里提问浪费时间啦！","https://www.baidu.com","http://www.baidu.com/img/bd_logo1.png", atAll=True)
    # d.sendActionCard("标题",
    #                  "![screenshot](@lADOpwk3K80C0M0FoA)\n### 乔布斯20年前想打造一间苹果咖啡厅，而它正是AppleStore的前身 @18079637336",
    #                  [
    #                      ("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
    #                      ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")
    #                  ], "18079637336")
    #
    # d.sendFeedCard([
    #     ("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
    #      "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
    #     ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
    #     ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
    #     ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")
    # ], atAll=True)

