import datetime
import time


def dateformat(timeObject, formatter: str = "%Y-%m-%d %H:%M:%S"):
    """
    格式化日期
    :param timeObject: 时间对象
    :param formatter:
        %y 两位数的年份表示（00-99）
        %Y 四位数的年份表示（000-9999）
        %m 月份（01-12）
        %d 月内中的一天（0-31）
        %H 24小时制小时数（0-23）
        %I 12小时制小时数（01-12）
        %M 分钟数（00-59）
        %S 秒（00-59）
        %f 毫秒
    :return:
    """
    if isinstance(timeObject, time.struct_time):
        return time.strftime(formatter, timeObject)
    if isinstance(timeObject, datetime.datetime):
        return timeObject.strftime(formatter)
    if isinstance(timeObject, datetime.date):
        return timeObject.strftime(formatter)
    raise ValueError("timeObject type error.")


def getYearCalendar(year: int):
    """
    获取某一年的日历信息
    :param year: 年份 例如：2020
    :return:
    """
    import calendar
    return calendar.calendar(year)


def getMonthCalendar(year: int, month: int):
    """
    获取某一年某个月份的日历信息
    :param year: 年份 例如：2020
    :param month: 月份 例如：10
    :return:
    """
    import calendar
    return calendar.month(year, month)


def currentTimeSeconds() -> int:
    """
    获取当前系统时间的时间戳（秒数）
    :return:
    """
    return int(time.time())


def currentTimeMillis() -> int:
    """
    获取当前系统时间的时间戳（毫数）
    :return:
    """
    return int(time.time() * 1000)


def currentTimeNanoseconds() -> int:
    """
    获取当前系统时间的时间戳（纳数）
    :return:
    """
    return time.time_ns()


def timestamp2datetime(timestamp: (int, float)):
    """
    时间戳转时间对象datetime
    :param timestamp:  时间戳（支持秒、毫秒、纳秒）
    :return: datetime对象
    """
    if timestamp > 10000000000:
        timestamp = timestamp / 1000
    if timestamp > 10000000000000:
        timestamp = timestamp / 1000000
    return datetime.datetime.fromtimestamp(timestamp)


def localtime():
    """
    当前时间
    :return:
    """
    return datetime.datetime.now()


def now():
    """
    当前时间
    :return:
    """
    return datetime.datetime.now()


def today():
    """
    获取当前日期
    :return:
    """
    return datetime.date.today()


def nowString(formatter: str = "%Y-%m-%d %H:%M:%S"):
    """
    当前时间字符串
    @:param formatter 格式化
    :return:
    """
    return dateformat(now(), formatter=formatter)


def todayString():
    return dateformat(today(), "%Y-%m-%d")


def getDateTime(year, month, day, hour=0, minute=0, second=0, microSecond=0):
    return datetime.datetime(year, month, day, hour, minute, second, microSecond)


def getDate(year: int, month: int, day: int):
    return datetime.date(year, month, day)


def getYear(dt: datetime = now()):
    return dt.year


def getMonth(dt: datetime = now()):
    return dt.month


def getDays(dt: datetime = now()):
    return dt.day


def getHours(dt: datetime = now()):
    return dt.hour


def getMinutes(dt: datetime = now()):
    return dt.minute


def getSeconds(dt: datetime = now()):
    return dt.second


def parse(dateString, formatter: str = "%Y-%m-%d %H:%M:%S"):
    """
    解析日期时间字符串
    :param dateString: 日期时间字符串
    :param formatter: 默认格式 "%Y-%m-%d %H:%M:%S"
    :return:
    """
    return datetime.datetime.strptime(dateString, formatter)


def parseDate(dateString, formatter: str = "%Y-%m-%d"):
    """
    解析日期字符串
    :param dateString: 日期时间字符串
    :param formatter: 默认格式 "%Y-%m-%d"
    :return:
    """
    return parse(dateString, formatter)


def parseDateTime(dateString, formatter: str = "%Y-%m-%d %H:%M:%S"):
    """
    解析日期时间字符串
    :param dateString: 日期时间字符串
    :param formatter: 默认格式 "%Y-%m-%d %H:%M:%S"
    :return:
    """
    return parse(dateString, formatter)


def parseTime(timeString, formatter: str = "%H:%M:%S"):
    """
    解析时间字符串
    :param timeString: 时间字符串
    :param formatter: 默认格式 "%H:%M:%S"
    :return:
    """
    return parse(timeString, formatter)


def toDateString(timeObject):
    """
    日期字符串 （格式："%Y-%m-%d）
    :param timeObject: 日期时间对象
    :return: 日期格式字符串
    """
    return dateformat(timeObject, "%Y-%m-%d")


def toDateTimeString(timeObject):
    """
    日期时间字符串 （格式：%Y-%m-%d %H:%M:%S）
    :param timeObject: 日期时间对象
    :return: 日期时间字符串
    """
    return dateformat(timeObject, formatter="%Y-%m-%d %H:%M:%S")


def toTimeStampString(timeObject, formatter: str = "%Y-%m-%d %H:%M:%S.%f"):
    """
    日期时间字符串 （格式：%Y-%m-%d %H:%M:%S.%f）
    :param timeObject: 日期时间对象
    :param formatter: 默认格式 %Y-%m-%d %H:%M:%S.%f
    :return: 日期时间字符串
    """
    if isinstance(timeObject, (int, float)):
        timeObject = timestamp2datetime(timeObject)
    return dateformat(timeObject, formatter)


def toDateTime(t: (time.struct_time, datetime.date, datetime.datetime, str)):
    """
    转换成datetime日期时间对象
    :param t: 时间对象或者字符串
    :return: datetime对象
    """
    if isinstance(t, datetime.datetime):
        return t
    if isinstance(t, datetime.date):
        return datetime.datetime(t.year, t.month, t.day)
    if isinstance(t, time.struct_time):
        return datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    if isinstance(t, str):
        return parseDateTime(t)


def plusTime(dt: datetime = now(), days=0, hours=0, minutes=0, seconds=0, millis=0):
    """
    日期时间加法
    :param dt: 基础时间，默认当前时间
    :param days: 天数
    :param hours: 小时
    :param minutes: 分钟
    :param seconds: 秒
    :param millis: 毫秒
    :return: datetime日期时间对象
    """
    return dt + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds,
                                   milliseconds=millis)


def plusDays(dt: datetime = now(), days=None):
    """
    日期时间加上多少天
    :param dt: 基础时间
    :param days: 加天数
    :return:
    """
    if days:
        return dt + datetime.timedelta(days=days)


def plusHours(dt: datetime = now(), hours=None):
    """
    日期时间加上多少小时
    :param dt: 基础时间
    :param hours: 加小时
    :return:
    """
    if hours:
        return dt + datetime.timedelta(hours=hours)


def plusMinutes(dt: datetime = now(), minutes=None):
    """
    日期时间加上多少分钟
    :param dt: 基础时间
    :param minutes: 加分钟
    :return:
    """
    if minutes:
        return dt + datetime.timedelta(minutes=minutes)


def plusSeconds(dt: datetime = now(), seconds=None):
    """
    日期时间加上多少秒
    :param dt: 基础时间
    :param seconds: 加秒
    :return:
    """
    if seconds:
        return dt + datetime.timedelta(seconds=seconds)
    return dt
