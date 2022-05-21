def _fcolor(msg, m=0, fg=None, bg=None):
    """
    格式化颜色字符串
    :param msg: 文本下次
    :param m: 模式
        0：默认，1：高亮显示，4：下划线，5：闪烁，7：反白显示，8：不可见
    :param fg: 前置色
    :param bg: 背景色
            30	40	黑色
            31	41	红色
            32	42	绿色
            33	43	黄色
            34	44	蓝色
            35	45	紫红色
            36	46	青蓝色
            37	47	白色
    :return:
    """
    if fg and bg:
        return f"\033[{m};{fg};{bg}m{msg}\033[m"
    elif fg or bg:
        return f"\033[{m};{fg or bg}m{msg}\033[m"
    else:
        return f"\033[{m}m{msg}\033[m"


class Logger(object):

    def __init__(self, tag: str = None, file: str = None, encoding: str = "utf-8", color: bool = False, **keywords):
        self.__color = color
        self.__tag = tag
        self.__internal = False
        self.__file = file
        self.__encoding = encoding
        if file:
            import datetime, os
            time = datetime.datetime.now().strftime("%Y-%m-%d")
            userHome = os.path.expanduser('~')
            desktop = os.path.join(userHome, "Desktop")
            file = file.format_map(
                {"time": time, "date": time, "userHome": userHome, "home": userHome, "desktop": desktop})
            self.__file = file
        if keywords and keywords.__contains__("internal"):
            self.__internal = keywords["internal"]

    def debug(self, msg: str, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        self.log(msg, level="DEBUG")

    def info(self, msg: str, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        self.log(msg, level="INFO")

    def warn(self, msg: str, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        self.log(msg, level="WARN")

    def error(self, msg: str, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        self.log(msg, level="ERROR")

    def success(self, msg: str, *args, **kwargs):
        msg = msg.format(*args, **kwargs)
        self.log(msg, level="OK")

    def log(self, msg, level: str = "INFO", color: bool = None):
        """
        打印日志
        :param msg: 消息
        :param level: 自定义日志等级
        :param color: 是否打印颜色（TRUE/FALSE）
        :return:
        """
        import datetime, os, threading, sys
        level = level.upper()
        pid = os.getpid()
        datetimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        pidStr = _fcolor(pid, fg=35)
        levelStr = _fcolor("%5s" % level, m=1)
        threadName = threading.currentThread().getName().lower()

        f = sys._getframe().f_back
        if self.__internal:
            f = f.f_back
        fileName = os.path.basename(f.f_code.co_filename)
        lineNo = f.f_lineno
        methodName = os.path.basename(f.f_code.co_name)
        if hasattr(f.f_back, 'f_code'):
            f = f.f_back
            fileName = os.path.basename(f.f_code.co_filename)
            lineNo = f.f_lineno
            methodName = os.path.basename(f.f_code.co_name)

        if methodName == '<module>':
            methodName = ''

        colorMsg = msg
        if level == 'ERROR' or level == 'FAIL':
            colorMsg = _fcolor(msg, fg=31)
        if level == 'WARN':
            colorMsg = _fcolor(msg, fg=33)
        if level == 'OK' or level == 'SUCCESS':
            colorMsg = _fcolor(msg, fg=32)
        if level == 'DEBUG':
            colorMsg = _fcolor(msg, fg=37)

        tagStr = ""
        if self.__tag and len(self.__tag) > 0:
            tagStr = f" ({self.__tag})"

        if color is None:
            color = self.__color
        if color:
            colorLog = "%s %s %s <%s> - [%s:%s:%s]%s : %s" % (
                datetimeStr, levelStr, pidStr, _fcolor(threadName, fg=34), _fcolor(fileName, fg=36), methodName, lineNo,
                _fcolor(tagStr, 1), colorMsg)
            print(colorLog)
            if self.__file:
                log = "%s %5s %s <%s> - [%s:%s:%s]%s : %s" % (
                    datetimeStr, level, pid, threadName, fileName, methodName, lineNo, tagStr, msg)
                self.__writeLogFile(log)
        else:
            log = "%s %5s %s <%s> - [%s:%s:%s]%s : %s" % (
                datetimeStr, level, pid, threadName, fileName, methodName, lineNo, tagStr, msg)
            print(log)
            self.__writeLogFile(log)

    def enablePrintColor(self):
        self.__color = True

    def disablePrintColor(self):
        self.__color = False

    def enableColor(self):
        self.__color = True

    def disableColor(self):
        self.__color = False

    def __writeLogFile(self, line):
        try:
            file = self.__file
            if not file:
                return
            import os
            if not os.path.exists(file):
                dir = os.path.abspath(os.path.dirname(file))
                if not os.path.exists(dir):
                    os.makedirs(dir)
            with open(file, 'a+', encoding=self.__encoding) as fd:
                fd.write(line)
                fd.write("\n")
                fd.close()
        except Exception:
            pass


class ColorLogger(Logger):
    def __init__(self, tag: str = None, file: str = None, encoding: str = "utf-8", **keywords):
        super().__init__(tag, file, encoding, True, **keywords)


"""
默认打印颜色
"""
__log = ColorLogger(internal=True)


def getLogger():
    return __log


def enablePrintColor():
    __log.enablePrintColor()


def disablePrintColor():
    __log.disablePrintColor()


def enableColor():
    __log.enablePrintColor()


def disableColor():
    __log.disablePrintColor()


def debug(msg: str, *args, **kwargs):
    __log.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs):
    __log.info(msg, *args, **kwargs)


def warn(msg: str, *args, **kwargs):
    __log.warn(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs):
    __log.error(msg, *args, **kwargs)


def success(msg: str, *args, **kwargs):
    __log.success(msg, *args, **kwargs)


def log(msg, level: str = "INFO", color: bool = None):
    """
    打印日志
    :param msg: 消息
    :param level: 自定义日志等级
    :param color: 是否打印颜色（TRUE/FALSE）
    :return:
    """
    __log.log(msg, level, color)
