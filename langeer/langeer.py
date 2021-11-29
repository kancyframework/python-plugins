def isString(value) -> bool:
    return isinstance(value, str)


def isBool(value) -> bool:
    return isinstance(value, bool)


def isInt(value) -> bool:
    return isinstance(value, int)


def isFloat(value) -> bool:
    return isinstance(value, float)


def isNumber(value) -> bool:
    return isInt(value) or isFloat(value)


def isList(value) -> bool:
    return isinstance(value, list)


def isSet(value) -> bool:
    return isinstance(value, set)


def isTuple(value) -> bool:
    return isinstance(value, tuple)


def isArray(value) -> bool:
    return isTuple(value)


def isByteArray(value) -> bool:
    return isinstance(value, (bytes, bytearray))


def isCollection(value) -> bool:
    return isinstance(value, (list, set, tuple))


def isDict(value) -> bool:
    return isinstance(value, dict)


def isMap(value) -> bool:
    return isDict(value)


def isClass(value) -> bool:
    return type(value).__name__ == 'type' and str(value).startswith("<class '")


def isBaseType(value) -> bool:
    return isinstance(value, (int, float, bool, str, dict, tuple, list, set, bytes, bytearray, complex))


def getClassName(value) -> str:
    if isClass(value):
        return value.__name__
    else:
        return type(value).__name__


def findClass(className):
    return forClass(className)


def forClass(className):
    import sys
    cls = None
    stop = False
    f = sys._getframe()
    while not stop:
        if f.f_globals.__contains__(className):
            c = f.f_globals[className]
            if isClass(c):
                cls = c
                break
        if f.f_globals['__name__'] == '__main__':
            stop = True
        f = f.f_back
    return cls


def isNull(obj) -> bool:
    return obj is None


def notNull(obj) -> bool:
    return not isNull(obj)


def isEmpty(obj) -> bool:
    if isNull(obj):
        return True
    if isinstance(obj, str):
        return obj == ""
    elif isinstance(obj, (list, set, tuple, dict)):
        return len(obj) < 1
    else:
        return False


def isNotEmpty(obj) -> bool:
    return not isEmpty(obj)


def notEmpty(obj) -> bool:
    return not isEmpty(obj)


def isAllEmpty(*args) -> bool:
    """
    所有元素都是空的
    :param args: 元素列表
    :return: True/False
    """
    if args:
        for arg in args:
            if isNotEmpty(arg):
                return False
        return True
    return True


def isNotAllEmpty(*args) -> bool:
    """
    所有元素都不是空的
    :param args: 元素列表
    :return: True/False
    """
    return not isAllEmpty(args)


def isBlank(obj) -> bool:
    if isNull(obj):
        return True
    if isinstance(obj, str):
        return obj.strip() == ""
    elif isinstance(obj, (list, set, tuple, dict)):
        return len(obj) < 1
    else:
        return False


def isNotBlank(obj) -> bool:
    return not isBlank(obj)


def notBlank(obj) -> bool:
    return isNotBlank(obj)


def assertTrue(obj, message=None):
    if not obj:
        raise AssertionError(message or "assert is true, but value is False")


def assertFalse(obj, message=None):
    if obj:
        raise AssertionError(message or f"assert is false, but value[{obj}] is True")


def assertEmpty(obj, message=None):
    if isNotEmpty(obj):
        raise AssertionError(message or f"assert is empty, but value[{obj}] is not empty")


def assertNotEmpty(obj, message=None):
    if isEmpty(obj):
        raise AssertionError(message or "assert not empty, but value is empty")


def assertBlank(obj, message=None):
    if isNotBlank(obj):
        raise AssertionError(message or f"assert is blank, but value[{obj}] is not blank")


def assertNotBlank(obj, message=None):
    if isBlank(obj):
        raise AssertionError(message or "assert not blank, but value is blank")


def obj2dict(obj, recursive=True):
    """把Object对象转换成Dict对象"""
    try:
        obj_dict = obj.__dict__
    except:
        return obj
    ret_obj_dict = {}
    ret_obj_dict.update(obj_dict)
    if recursive:
        for field in obj_dict:
            fieldValue = obj_dict[field]
            if not isBaseType(fieldValue):
                ret_obj_dict[field] = obj2dict(fieldValue)
    return ret_obj_dict


def dict2obj(mapping: dict, obj):
    """
    将字段的属性赋值给对象
    :param mapping: 字典
    :param obj: 对象实例、类型、类名
    :return:
    """
    if isClass(obj):
        obj = obj()
    elif isinstance(obj, str):
        objClass = forClass(obj)
        if objClass:
            obj = objClass()
        else:
            raise RuntimeError(f"Not Found class : {obj}")
    try:
        obj.__dict__.update(mapping)
    except:
        pass
    return obj
