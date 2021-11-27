import random


def randomUuid() -> str:
    """
    生成随机的uuid
    :return: 随机的uuid
    """
    import uuid
    return str(uuid.uuid3(uuid.uuid4(), str(uuid.uuid1())))


def randomInt(start: int = 0, end: int = 100, step=None) -> int:
    """
    随机生成指定范围内的整数
    :param start: 开始范围
    :param end: 结束范围
    :param step: 步长
    :return: 随机整数
    """
    if step:
        return random.randrange(start, end, step)
    return random.randint(start, end)


def randomFloat(start: float = 0, end: float = 1, scale=None) -> float:
    """
    随机生成指定范围内的浮点数
    :param start: 开始范围
    :param end: 结束范围
    :param scale: 精度
    :return:
    """
    if scale and scale > 0:
        return round(random.uniform(start, end), scale)
    return random.uniform(start, end)


def randomItem(items: (list, set, tuple, str)):
    """
    随机一个元素
    :param items: 元素集合
    :return: 随机一个元素
    """
    if items:
        return random.choice(items)


def randomItems(items: (list, set, tuple, str), size=1, distinct=True) -> list:
    """
    随机一个元素列表
    :param items: 元素集合
    :param size: 随机个数
    :param distinct: 是否去重
    :return: 随机元素列表
    """
    if items:
        if distinct:
            items = list(set(items))
            if 0 < size == len(items):
                random.shuffle(items)
                return items
            if 0 < size < len(items):
                lists = []
                while len(lists) < size:
                    it = random.choice(items)
                    if not lists.__contains__(it):
                        lists.append(it)
                return lists
            else:
                raise RuntimeError("distinct item len < random size")
        else:
            if size > 0:
                lists = []
                while len(lists) < size:
                    lists.append(random.choice(items))
                return lists


def randomChars(size: int, distinct=False) -> str:
    """
    随机生成指定长度的可见字符串
    :param size:
    :param distinct:
    :return:
    """
    items = []
    items.extend(range(48, 57))
    items.extend(range(65, 90))
    items.extend(range(97, 122))
    random.shuffle(items)
    rItems = randomItems(items, size, distinct)
    return "".join([chr(item) for item in rItems])


def randomMobile(*pres) -> str:
    """
    随机生成手机号
        randomMobile(180,136,185)
    :param pres:手机号前缀
    :return: 手机号码
    """
    preStr = "1"
    if pres:
        preStr = str(randomItem(pres))
    randomSize = 11 - len(preStr)
    if randomSize > 0:
        return preStr + "".join(randomItems("0123456789", randomSize))
    else:
        return preStr[0:11]


def randomMobiles(*pres, size: int = 1) -> list[str]:
    """
    随机生成一批手机号
        randomMobiles(180,136,185, size=10)
    :param pres:手机号前缀
    :param size:批量大小
    :return: 手机号码
    """
    mobiles = set()
    if size <= 0:
        return []
    while len(mobiles) < size:
        mobiles.add(randomMobile(*pres))
    return list(mobiles)
