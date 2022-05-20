def getRedis(host="localhost",
             port=6379,
             db=0,
             password=None, **kwargs):
    """
    获取redis对象
    :param host: 地址
    :param port: 端口
    :param db: 数据库
    :param password: 密码
    :param kwargs: 其他属性
    :return:
    """
    import redis
    redis_conn = redis.Redis(host=host, port=port, db=db, password=password, **kwargs)
    return redis_conn


def getSimpleRedis(host="localhost",
                   port=6379,
                   db=0,
                   password=None, **kwargs):
    """
    获取redis对象
    :param host: 地址
    :param port: 端口
    :param db: 数据库
    :param password: 密码
    :param kwargs: 其他属性
    :return:
    """
    return SimpleRedis(host=host, port=port, db=db, password=password, **kwargs)


class SimpleRedis:
    def __init__(self, host="localhost",
                 port=6379,
                 db=0,
                 password=None, **kwargs):
        self.__redis_conn = getRedis(host, port, db, password, **kwargs)

    def __new_value(self, value):
        """
        底层只支持：bytes, string, int or float
        """
        if isinstance(value, (bytes, str, int, float)):
            return value
        import jsoneer
        return jsoneer.toJsonString(value)

    def set(self, key: str, value):
        value = self.__new_value(value)
        conn = self.__redis_conn
        return conn.set(name=key, value=value)

    def setex(self, key: str, value, second: int):
        """
        设置带过期时间的值
        """
        second = int(second)
        value = self.__new_value(value)
        conn = self.__redis_conn
        if second > 0:
            return conn.setex(name=key, value=value, time=second)
        return conn.set(name=key, value=value)

    def setnx(self, key: str, value):
        """
        Setnx（SET if Not eXists） 命令在指定的 key 不存在时，为 key 设置指定的值
        """
        value = self.__new_value(value)
        conn = self.__redis_conn
        return conn.setnx(name=key, value=value)

    def get(self, key: str, def_value=None):
        conn = self.__redis_conn
        value = conn.get(name=key)
        if value:
            import jsoneer
            try:
                return jsoneer.readJson(value)
            except Exception:
                return value
        return def_value

    def delete(self, *keys: str):
        conn = self.__redis_conn
        return conn.delete(*keys)

    def incr(self, key: str, amount: int = 1):
        """
        Increments the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as ``amount``

        For more information see https://redis.io/commands/incrby
        """
        conn = self.__redis_conn
        return conn.incr(name=key, amount=amount)

    def decr(self, key: str):
        """
        Decrements the value of ``key`` by ``amount``.  If no key exists,
        the value will be initialized as 0 - ``amount``

        For more information see https://redis.io/commands/decrby
        """
        conn = self.__redis_conn
        return conn.decr(name=key)

    def hmset(self, name: str, mapping: dict):
        conn = self.__redis_conn
        return conn.hmset(name=name, mapping=mapping)

    def hmget(self, name: str, keys: list, *args):
        conn = self.__redis_conn
        return conn.hmget(name=name, keys=keys, *args)

    def options(self):
        return self.__redis_conn

    def close(self):
        return self.__redis_conn.close()
