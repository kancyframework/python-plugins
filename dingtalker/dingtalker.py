import base64
import hashlib
import hmac
import re
import time
import os

import requests


class DingTalkClient:
    """
    dingTalkClient = DingTalkClient(accessToken,secretKey)
    dingTalkClient.sendText()
    """

    def __init__(self, accessToken: str, secretKey: str = None, encoding="utf-8", debug: bool = False) -> None:
        self.secretKey = secretKey
        self.accessToken = accessToken
        self.encoding = encoding
        self.debug = debug

    def sendText(self, content: str, at: (list, set, tuple, str) = None, atAll: bool = False, headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        """
        jsonBody = {
            "msgtype": "text",
            "text": {
                "content": f"{content}"
            },
            "at": {"atMobiles": self.__toList(at), "isAtAll": atAll}}
        return self.send(jsonBody, headers)

    def sendMarkdown(self, title: str, markdownText: str, at: (list, set, tuple, str) = None, atAll: bool = False,
                     headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        """
        jsonBody = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"{markdownText}"
            },
            "at": {"atMobiles": self.__toList(at), "isAtAll": atAll}}
        return self.send(jsonBody, headers)

    def sendLink(self, title: str, text: str, messageUrl: str, picUrl: str, at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        """
        jsonBody = {
            "msgtype": "link",
            "link": {
                "title": f"{title}",
                "text": f"{text}",
                "messageUrl": f"{messageUrl}",
                "picUrl": f"{picUrl}",
            },
            "at": {"isAtAll": atAll, "atMobiles": self.__toList(at)}
        }
        return self.send(jsonBody, headers)

    def sendActionCard(self, title: str, text: str, btns: (list, set, tuple) = None, at: (list, set, tuple, str) = None,
                       atAll: bool = False,
                       headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        :btns 格式 : [
                         ("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                         ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")
                    ]
        """
        realBtns = []
        if btns:
            for btn in btns:
                if isinstance(btn, dict):
                    realBtns.append(btn)
                if isinstance(btn, (list, tuple)) and len(btn) == 2:
                    realBtns.append({"title": f"{btn[0]}", "actionURL": f"{btn[1]}"})
        at = self.__toList(at)

        jsonBody = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": f"{title}",
                "text": f"{text}",
                "btns": realBtns,
                "btnOrientation": "1",
                "hideAvatar": "0"
            },
            "at": {"isAtAll": atAll, "atMobiles": self.__toList(at)}
        }
        return self.send(jsonBody, headers)

    def sendFeedCard(self, links: (list, set, tuple), at: (list, set, tuple, str) = None, atAll: bool = False,
                     headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        :links 格式 : [
                        ("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
                         "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
                        ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
                        ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
                        ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")
                    ]
        """
        realLinks = []
        if links:
            for link in links:
                if isinstance(link, dict):
                    realLinks.append(link)
                if isinstance(link, (list, tuple)):
                    if len(link) == 3:
                        realLinks.append({"title": f"{link[0]}", "messageURL": f"{link[1]}", "picURL": f"{link[2]}"})
                    if len(link) == 2:
                        realLinks.append({"title": f"{link[0]}", "messageURL": f"{link[1]}"})
        jsonBody = {
            "msgtype": "feedCard",
            "feedCard": {
                "links": realLinks
            },
            "at": {"isAtAll": atAll, "atMobiles": self.__toList(at)}}
        return self.send(jsonBody, headers)

    def send(self, jsonBody, headers=None):
        if not headers:
            headers = {"Content-Type": "application/json ;charset=utf-8 "}
        url = self.__getServiceUrl()
        response = requests.post(url, headers=headers, json=jsonBody, timeout=(3, 60))
        if self.debug and response:
            print(f"请求报文：{jsonBody}\n返回报文：{response.text}")
        return response

    def getServiceUrl(self, accessToken: str, secretKey: str = None) -> str:
        url = f"https://oapi.dingtalk.com/robot/send?access_token={accessToken}"
        if secretKey:
            # 加密，获取sign和timestamp
            timestamp = int(round(time.time() * 1000))
            secretDataBytes = (str(timestamp) + '\n' + self.secretKey).encode('utf-8')
            secretBytes = self.secretKey.encode('utf-8')
            signature = base64.b64encode(hmac.new(secretBytes, secretDataBytes, digestmod=hashlib.sha256).digest())
            reg = re.compile(r"'(.*)'")
            sign = str(re.findall(reg, str(signature))[0])
            url = f"{url}&sign={sign}&timestamp={timestamp}"
        return url

    def __getServiceUrl(self) -> str:
        return self.getServiceUrl(self.accessToken, self.secretKey)

    def __toList(self, at: (list, set, tuple, str) = None):
        ats = []
        if at:
            if isinstance(at, str):
                ats.extend(at.split(","))
            if isinstance(at, (list, set, tuple)):
                ats.extend(at)
        return ats


class DingTalker:
    """
    dingTalker = DingTalker(configFilePath)
    dingTalker.sendText()

    configFilePath 默认路径 'dingtalker.ini', 'dingtalk-client.ini', 'dingtalk.ini' , client is test、test1、test2
        [test]
        accessToken=1676877387c8a486a8c81491def78a931d0a7df65e3eff0c3ef28c4a25b5cc5
        secretKey=SEC92e1603e992a14af2b27efdb6753bf08eadc694ee6dfc9cb458327899dbd269
        debug=True

        [test1]
        accessToken=1676877387c8a486a8c81491def78a931d0a7df65e3eff0c3ef28c4a25b5cc5
        secretKey=SEC92e1603e992a14af2b27efdb6753bf08eadc694ee6dfc9cb458327899dbd269
        debug=False

        [test2]
        accessToken=1676877387c8a486a8c81491def78a931d0a7df65e3eff0c3ef28c4a25b5cc5
        secretKey=SEC92e1603e992a14af2b27efdb6753bf08eadc694ee6dfc9cb458327899dbd269
        debug=True
        encoding=GBK
    """

    def __init__(self, configFilePath: str = None, encoding="utf-8") -> None:
        import confer

        if not configFilePath:
            files = ['dingtalker.ini', 'dingtalk-client.ini', 'dingtalk.ini']
            for file in files:
                if os.access(file, os.F_OK):
                    configFilePath = file
                    break
        if not configFilePath:
            raise RuntimeError(f"Not Found conf file : {files}")

        self.configFilePath = configFilePath
        self.encoding = encoding
        self.confer = confer.Confer(configFilePath, encoding)
        self.dingTalkClients = {}

    def sendText(self, client: str, content: str, at: (list, set, tuple, str) = None, atAll: bool = False,
                 headers=None):
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendText(content, at, atAll, headers)

    def sendMarkdown(self, client: str, title: str, markdownText: str, at: (list, set, tuple, str) = None,
                     atAll: bool = False,
                     headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendMarkdown(title, markdownText, at, atAll, headers)

    def sendLink(self, client: str, title: str, text: str, messageUrl: str, picUrl: str,
                 at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendLink(title, text, messageUrl, picUrl, at, atAll, headers)

    def sendActionCard(self, client: str, title: str, text: str, btns: (list, set, tuple) = None,
                       at: (list, set, tuple, str) = None,
                       atAll: bool = False,
                       headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        :btns 格式 : [
                         ("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                         ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")
                    ]
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendActionCard(title, text, btns, at, atAll, headers)

    def sendFeedCard(self, client: str, links: (list, set, tuple), at: (list, set, tuple, str) = None,
                     atAll: bool = False,
                     headers=None):
        """
        :at 参数可以是数组，也可以是使用逗号分隔的字符串
        :links 格式 : [
                        ("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
                         "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
                        ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
                        ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
                        ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")
                    ]
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendFeedCard(links, at, atAll, headers)

    def send(self, client: str, jsonBody, headers=None):
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.send(jsonBody, headers)

    def __findDingTalkClient(self, client) -> DingTalkClient:
        dingTalkClient = self.dingTalkClients.get(client)
        if not dingTalkClient:
            dingTalkClient = self.__initDingTalkClient(client)
        return dingTalkClient

    def __initDingTalkClient(self, client) -> DingTalkClient:
        accessToken = self.confer.get(client, 'accessToken')
        secretKey = self.confer.get(client, 'secretKey')
        if accessToken and secretKey:
            encoding = self.confer.get(client, 'encoding', self.encoding)
            debug = self.confer.getBoolean(client, 'debug', False)
            dingTalkClient = DingTalkClient(accessToken, secretKey, encoding, debug)
            return dingTalkClient
        raise RuntimeError(f"In {self.configFilePath} , Not Found client {client} -> accessToken and secretKey")
