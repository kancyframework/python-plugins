import base64
import datetime
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
        发送普通文本消息
        :param client: 客户端
        :param content: 文本内容
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
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
          发送markdown富文本消息
          :param title: 消息标题
          :param markdownText: markdown内容
          :param at: @某人 数组/字符串
              如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
          :param atAll: 是否@所有人
          :param headers: 额外请求头信息，通用不用关心
          :return:
          """
        jsonBody = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"{markdownText}"
            },
            "at": {"atMobiles": self.__toList(at), "isAtAll": atAll}}
        return self.send(jsonBody, headers)

    def sendMarkdownFile(self, title: str, filePath: str, at: (list, set, tuple, str) = None, atAll: bool = False,
                         encoding: str = 'utf-8', **templateVariables):
        """
        发送markdown富文本消息（模板文件）
        :param title: 消息标题
        :param filePath: markdown模板文件内容
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param encoding: 模板文件编码
        :param templateVariables: 模板变量
        :return:
        """
        if os.path.exists(filePath) and os.path.isfile(filePath):
            with open(filePath, 'r', encoding=encoding) as f:
                markdownFileData = f.read()
            if len(markdownFileData.strip()) > 0:
                newTemplateVariables = dict(templateVariables)
                newTemplateVariables['__title'] = title
                newTemplateVariables['__filePath'] = os.path.abspath(filePath)
                newTemplateVariables['__at'] = at
                newTemplateVariables['__atAll'] = atAll
                newTemplateVariables['__encoding'] = encoding
                newTemplateVariables['__today'] = datetime.date.today().strftime("%Y-%m-%d")
                markdownText = markdownFileData.format_map(newTemplateVariables)
                del newTemplateVariables
                return self.sendMarkdown(title, markdownText, at, atAll)
            raise FileNotFoundError(f"file content is blank : {filePath}")
        raise FileNotFoundError(f"file not found : {filePath}")

    def sendLink(self, title: str, text: str, messageUrl: str, picUrl: str, at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
        """
        发送Link钉钉消息
        :param title: 消息标题
        :param text: 文本内容
        :param messageUrl: 消息跳转链接
        :param picUrl: 消息的图片地址
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
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

    def sendActionCard(self, title: str, markdownText: str, btns: (list, set, tuple) = None,
                       at: (list, set, tuple, str) = None,
                       atAll: bool = False,
                       headers=None):
        """
        发送ActionCard钉钉消息
        :param title: 消息标题
        :param markdownText: 文本内容
        :param btns: 按钮列表
            格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                   ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
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
                "text": f"{markdownText}",
                "btns": realBtns,
                "btnOrientation": "1",
                "hideAvatar": "0"
            },
            "at": {"isAtAll": atAll, "atMobiles": self.__toList(at)}
        }
        return self.send(jsonBody, headers)

    def sendActionCardFile(self, title: str, filePath: str, btns: (list, set, tuple) = None,
                           at: (list, set, tuple, str) = None,
                           atAll: bool = False, encoding: str = 'utf-8', **templateVariables):
        """
        发送ActionCard钉钉消息（模板文件）
        :param title: 消息标题
        :param filePath: markdown模板文件路径
        :param btns: 按钮列表
            格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                   ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param encoding: 模板文件编码
        :param templateVariables: 模板文件变量
        :return:
        """
        if os.path.exists(filePath) and os.path.isfile(filePath):
            with open(filePath, 'r', encoding=encoding) as f:
                markdownFileData = f.read()
            if len(markdownFileData.strip()) > 0:
                newTemplateVariables = dict(templateVariables)
                newTemplateVariables['__title'] = title
                newTemplateVariables['__filePath'] = os.path.abspath(filePath)
                newTemplateVariables['__at'] = at
                newTemplateVariables['__atAll'] = atAll
                newTemplateVariables['__btns'] = btns
                newTemplateVariables['__encoding'] = encoding
                newTemplateVariables['__today'] = datetime.date.today().strftime("%Y-%m-%d")
                markdownText = markdownFileData.format_map(newTemplateVariables)
                del newTemplateVariables
                return self.sendActionCard(title, markdownText, btns, at, atAll)
            raise FileNotFoundError(f"file content is blank : {filePath}")
        raise FileNotFoundError(f"file not found : {filePath}")

    def sendFeedCard(self, links: (list, set, tuple), at: (list, set, tuple, str) = None, atAll: bool = False,
                     headers=None):
        """
        发送FeedCard钉钉消息
        :param links: 图文链接列表
            格式 : [("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
                    "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
                    ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
                    ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
                    ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
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
        """
        发送钉钉消息请求
        :param jsonBody: 消息请求体
        :param headers: 请求头
        :return:
        """
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
            userHome = str(os.path.expanduser('~')).replace("\\", "/")
            files = ['dingtalker.ini', 'dingtalk-client.ini', 'dingtalk.ini',
                     f'{userHome}/dingtalker.ini', f'{userHome}/dingtalk-client.ini', f'{userHome}/dingtalk.ini']
            for file in files:
                if os.access(file, os.F_OK):
                    configFilePath = file
                    break
        else:
            # 用户指定的配置文件必须存在
            if not (os.path.exists(configFilePath) and os.path.isfile(configFilePath)):
                raise RuntimeError(f"Not access conf file : {configFilePath}")

        self.encoding = encoding
        self.dingTalkClients = {}
        self.configFilePath = None
        self.confer = None
        if configFilePath:
            self.configFilePath = configFilePath
            self.confer = confer.Confer(configFilePath, encoding)

    def sendText(self, client: str, content: str, at: (list, set, tuple, str) = None, atAll: bool = False,
                 headers=None):
        """
        发送普通文本消息
        :param client: 客户端
        :param content: 文本内容
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendText(content, at, atAll, headers)

    def sendMarkdown(self, client: str, title: str, markdownText: str, at: (list, set, tuple, str) = None,
                     atAll: bool = False,
                     headers=None):
        """
        发送markdown富文本消息
        :param client: 客户端
        :param title: 消息标题
        :param markdownText: markdown内容
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendMarkdown(title, markdownText, at, atAll, headers)

    def sendMarkdownFile(self, client: str, title: str, filePath: str, at: (list, set, tuple, str) = None,
                         atAll: bool = False,
                         encoding='utf-8', **templateVariables):
        """
        发送markdown富文本消息（模板文件）
        :param client: 客户端名称
        :param title: 消息标题
        :param filePath: markdown模板文件内容
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param encoding: 模板文件编码
        :param templateVariables: 模板变量
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendMarkdownFile(title, filePath, at, atAll, encoding, **templateVariables)

    def sendLink(self, client: str, title: str, text: str, messageUrl: str, picUrl: str,
                 at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
        """
        发送Link钉钉消息
        :param client: 客户端名称
        :param title: 消息标题
        :param text: 文本内容
        :param messageUrl: 消息跳转链接
        :param picUrl: 消息的图片地址
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendLink(title, text, messageUrl, picUrl, at, atAll, headers)

    def sendActionCard(self, client: str, title: str, markdownText: str, btns: (list, set, tuple) = None,
                       at: (list, set, tuple, str) = None,
                       atAll: bool = False,
                       headers=None):
        """
        发送ActionCard钉钉消息
        :param client: 客户端名称
        :param title: 消息标题
        :param markdownText: 文本内容
        :param btns: 按钮列表
            格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                   ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendActionCard(title, markdownText, btns, at, atAll, headers)

    def sendActionCardFile(self, client: str, title: str, filePath: str, btns: (list, set, tuple) = None,
                           at: (list, set, tuple, str) = None,
                           atAll: bool = False, encoding: str = 'utf-8', **templateVariables):
        """
        发送ActionCard钉钉消息（模板文件）
        :param client: 客户端名称
        :param title: 消息标题
        :param filePath: markdown模板文件路径
        :param btns: 按钮列表
            格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
                   ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param encoding: 模板文件编码
        :param templateVariables: 模板文件变量
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendActionCardFile(title, filePath, btns, at, atAll, encoding, **templateVariables)

    def sendFeedCard(self, client: str, links: (list, set, tuple), at: (list, set, tuple, str) = None,
                     atAll: bool = False,
                     headers=None):
        """
        发送FeedCard钉钉消息
        :param client: 客户端名称
        :param links: 图文链接列表
            格式 : [("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
                    "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
                    ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
                    ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
                    ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")]
        :param at: @某人 数组/字符串
            如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
        :param atAll: 是否@所有人
        :param headers: 额外请求头信息，通用不用关心
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.sendFeedCard(links, at, atAll, headers)

    def send(self, client: str, jsonBody, headers=None):
        """
        发送钉钉消息请求
        :param client: 客户端名称
        :param jsonBody: 消息请求体
        :param headers: 请求头
        :return:
        """
        dingTalkClient = self.__findDingTalkClient(client)
        if dingTalkClient:
            dingTalkClient.send(jsonBody, headers)

    def __findDingTalkClient(self, client) -> DingTalkClient:
        dingTalkClient = self.dingTalkClients.get(client)
        if not dingTalkClient:
            dingTalkClient = self.__initDingTalkClient(client)
            self.dingTalkClients[client] = dingTalkClient
        return dingTalkClient

    def __initDingTalkClient(self, client) -> DingTalkClient:
        if not self.confer or not self.confer.has(client):
            raise RuntimeError(f"Not Found client {client}")
        accessToken = self.confer.get(client, 'accessToken')
        secretKey = self.confer.get(client, 'secretKey')
        if accessToken and secretKey:
            encoding = self.confer.get(client, 'encoding', self.encoding)
            debug = self.confer.getBoolean(client, 'debug', False)
            dingTalkClient = DingTalkClient(accessToken, secretKey, encoding, debug)
            return dingTalkClient
        raise RuntimeError(f"In {self.configFilePath} , Not Found client {client} -> accessToken and secretKey")


__dingTalker = DingTalker()


def sendText(client: str, content: str, at: (list, set, tuple, str) = None, atAll: bool = False,
             headers=None):
    """
    发送普通文本消息
    :param client: 客户端
    :param content: 文本内容
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param headers: 额外请求头信息，通用不用关心
    :return:
    """
    __dingTalker.sendText(client, content, at, atAll, headers)


def sendMarkdown(client: str, title: str, markdownText: str, at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
    """
    发送markdown富文本消息
    :param client: 客户端
    :param title: 消息标题
    :param markdownText: markdown内容
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param headers: 额外请求头信息，通用不用关心
    :return:
    """
    __dingTalker.sendMarkdown(client, title, markdownText, at, atAll, headers)


def sendMarkdownFile(client: str, title: str, filePath: str, at: (list, set, tuple, str) = None,
                     atAll: bool = False,
                     encoding='utf-8', **templateVariables):
    """
    发送markdown富文本消息（模板文件）
    :param client: 客户端名称
    :param title: 消息标题
    :param filePath: markdown模板文件内容
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param encoding: 模板文件编码
    :param templateVariables: 模板变量
    :return:
    """
    __dingTalker.sendMarkdownFile(client, title, filePath, at, atAll, encoding, **templateVariables)


def sendLink(client: str, title: str, text: str, messageUrl: str, picUrl: str,
             at: (list, set, tuple, str) = None,
             atAll: bool = False,
             headers=None):
    """
    发送Link钉钉消息
    :param client: 客户端名称
    :param title: 消息标题
    :param text: 文本内容
    :param messageUrl: 消息跳转链接
    :param picUrl: 消息的图片地址
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param headers: 额外请求头信息，通用不用关心
    :return:
    """
    __dingTalker.sendLink(client, title, text, messageUrl, picUrl, at, atAll, headers)


def sendActionCard(client: str, title: str, markdownText: str, btns: (list, set, tuple) = None,
                   at: (list, set, tuple, str) = None,
                   atAll: bool = False,
                   headers=None):
    """
    发送ActionCard钉钉消息
    :param client: 客户端名称
    :param title: 消息标题
    :param markdownText: 文本内容
    :param btns: 按钮列表
        格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
               ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param headers: 额外请求头信息，通用不用关心
    :return:
    """
    __dingTalker.sendActionCard(client, title, markdownText, btns, at, atAll, headers)


def sendActionCardFile(client: str, title: str, filePath: str, btns: (list, set, tuple) = None,
                       at: (list, set, tuple, str) = None,
                       atAll: bool = False, encoding: str = 'utf-8', **templateVariables):
    """
    发送ActionCard钉钉消息（模板文件）
    :param client: 客户端名称
    :param title: 消息标题
    :param filePath: markdown模板文件路径
    :param btns: 按钮列表
        格式 : [("内容不错", "https://www.cnblogs.com/kancy/p/13470386.html"),
               ("不感兴趣", "https://www.cnblogs.com/kancy/p/13912443.html")]
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param encoding: 模板文件编码
    :param templateVariables: 模板文件变量
    :return:
    """
    __dingTalker.sendActionCardFile(client, title, filePath, btns, at, atAll, encoding, **templateVariables)


def sendFeedCard(client: str, links: (list, set, tuple), at: (list, set, tuple, str) = None,
                 atAll: bool = False,
                 headers=None):
    """
    发送FeedCard钉钉消息
    :param client: 客户端名称
    :param links: 图文链接列表
        格式 : [("定位占用CPU较高的进程、线程、代码位置？", "https://www.cnblogs.com/kancy/p/13470386.html",
                "https://img1.baidu.com/it/u=3312920655,3266355600&fm=26&fmt=auto"),
                ("浅谈我对DDD领域驱动设计的理解", "https://www.cnblogs.com/kancy/p/13425737.html"),
                ("单元测试之PowerMock", "https://www.cnblogs.com/kancy/p/13912443.html"),
                ("正确创建索引和索引失效", "https://www.cnblogs.com/kancy/p/13460140.html")]
    :param at: @某人 数组/字符串
        如果是字符串，使用逗号分隔，例如：180xxx001,180xxx002
    :param atAll: 是否@所有人
    :param headers: 额外请求头信息，通用不用关心
    :return:
    """
    __dingTalker.sendFeedCard(client, links, at, atAll, headers)


def send(client: str, jsonBody, headers=None):
    """
    发送钉钉消息请求
    :param client: 客户端名称
    :param jsonBody: 消息请求体
    :param headers: 请求头
    :return:
    """
    __dingTalker.send(client, jsonBody, headers)
