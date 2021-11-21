import calendar
import datetime
import time


def getYearCalendar(year: int):
    return calendar.calendar(year)


def getMonthCalendar(year: int, month: int):
    return calendar.month(year, month)


def currentTimeSeconds() -> int:
    return int(time.time())


def currentTimeMillis() -> int:
    return int(time.time() * 1000)


def currentTimeNanoseconds() -> int:
    return time.time_ns()


def localtime():
    return time.localtime()


def now():
    return datetime.datetime.now()


def nowString():
    return toString(now())


def today():
    return datetime.date.today()


def todayString():
    return toString(today(), "%Y-%m-%d")


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


def parse(date_string, formatter: str = "%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(date_string, formatter)


def parseDate(date_string, formatter: str = "%Y-%m-%d"):
    return parse(date_string, formatter)


def parseDateTime(date_string, formatter: str = "%Y-%m-%d %H:%M:%S"):
    return parse(date_string, formatter)


def parseTime(date_string, formatter: str = "%H:%M:%S"):
    return parse(date_string, formatter)


def toString(timeObject, formatter: str = "%Y-%m-%d %H:%M:%S"):
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
    :return:
    """
    if isinstance(timeObject, time.struct_time):
        return time.strftime(formatter, timeObject)
    if isinstance(timeObject, datetime.datetime):
        return timeObject.strftime(formatter)
    if isinstance(timeObject, datetime.date):
        return timeObject.strftime(formatter)
    raise ValueError("timeObject type error.")


def toDateString(timeObject):
    return toString(timeObject, "%Y-%m-%d")


def toDateTimeString(timeObject):
    return toString(timeObject)


def toDateTime(t: (time.struct_time, datetime.date, datetime.datetime, str)):
    if isinstance(t, datetime.datetime):
        return t
    if isinstance(t, datetime.date):
        return datetime.datetime(t.year, t.month, t.day)
    if isinstance(t, time.struct_time):
        return datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    if isinstance(t, str):
        return parseDateTime(t)


def plusTime(dt: datetime = now(), days=0, hours=0, minutes=0, seconds=0, millis=0):
    return dt + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds,
                                   milliseconds=millis)


def plusDays(dt: datetime = now(), days=None):
    if days:
        return dt + datetime.timedelta(days=days)


def plusHours(dt: datetime = now(), hours=None):
    if hours:
        return dt + datetime.timedelta(hours=hours)


def plusMinutes(dt: datetime = now(), minutes=None):
    if minutes:
        return dt + datetime.timedelta(minutes=minutes)


def plusSeconds(dt: datetime = now(), seconds=None):
    if seconds:
        return dt + datetime.timedelta(seconds=seconds)
    return dt
