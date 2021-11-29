import json


class __ObjectJsonEncoder(json.JSONEncoder):
    def default(self, o):
        import datetime, decimal
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, set):
            return list(o)
        elif isinstance(o, complex):
            return str(o)
        if isinstance(o, decimal.Decimal):
            return float(o)
        else:
            try:
                return o.__dict__
            except:
                return super().default(o)


def toJsonString(obj, pretty=False, ascii=False) -> str:
    """
    :param obj: 对象
    :param pretty: 是否格式化
    :param ascii: 汉字是否转换成ascii码
    :return:
    """
    indent = None
    if pretty:
        indent = 4
    import json
    return json.dumps(obj, cls=__ObjectJsonEncoder, ensure_ascii=ascii, indent=indent)


def toJson(obj, pretty=False) -> str:
    return toJsonString(obj, pretty=pretty)


def jsondumps(obj, pretty=False) -> str:
    return toJsonString(obj, pretty=pretty)


def readJsonString(jsonStr: str) -> dict:
    return json.loads(jsonStr)


def readJson(jsonStr: str) -> dict:
    return readJsonString(jsonStr)


def jsonloads(jsonStr: str) -> dict:
    return readJsonString(jsonStr)
