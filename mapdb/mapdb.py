class MapDB:
    """
    mapdb基类
    """
    from dber import DB

    def __init__(self, db: DB, topic='default') -> None:
        self.db = db
        self.__topic = topic
        self.__initDataTable()

    def __initDataTable(self):
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.__tableName()} (
                data_key varchar(255) PRIMARY KEY, 
                data_value blob
            ) 
            """
        self.db.execute(sql)

    def __tableName(self):
        return f"t_kv_{self.__topic}"

    def enableDebug(self):
        self.db.enableDebug()

    def disableDebug(self):
        self.db.disableDebug()

    def putBytes(self, key: str, byteArrays: bytes):
        if byteArrays:
            sql = f"REPLACE INTO {self.__tableName()}(data_key, data_value) values (?,?)"
            self.db.execute(sql, (key, byteArrays))

    def putFile(self, key: str, filePath: str):
        import os
        if os.path.exists(filePath) and os.path.isfile(filePath):
            with open(filePath, 'rb') as f:
                self.putBytes(key, f.read())

    def put(self, key: str, value):
        if isinstance(value, bytes):
            return self.putBytes(key, value)
        if isinstance(value, (int, float, str)):
            realValue = value
        else:
            import json
            realValue = json.dumps(value)
        sql = f"REPLACE INTO {self.__tableName()}(data_key, data_value) values (?,?)"
        self.db.execute(sql, (key, realValue))

    def puts(self, kv_items: dict):
        import json
        rows = []
        for key in kv_items:
            value = kv_items[key]
            if isinstance(value, (int, float, str, bytes)):
                realValue = value
            elif isinstance(value, set):
                realValue = json.dumps(list(value))
            else:
                realValue = json.dumps(value)
            rows.append((key, realValue))
        sql = f"REPLACE INTO {self.__tableName()}(data_key,data_value) values (?,?)"
        self.db.replaceBatch(sql, rows)

    def keys(self, limit: int = 0) -> list:
        rows = self.db.selectTable(self.__tableName(), "data_key", limit=limit)
        keys = []
        if rows:
            for row in rows:
                keys.append(row['data_key'])
        return keys

    def randomKeys(self, limit: int = 10) -> list:
        rows = self.db.selectTable(self.__tableName(), "data_key", where="1=1 order by random()", limit=limit)
        keys = []
        if rows:
            for row in rows:
                keys.append(row['data_key'])
        return keys

    def get(self, key: str, defValue=None):
        sql = f"SELECT data_value from {self.__tableName()} WHERE data_key = ?"
        result = self.db.selectOne(sql, key, hump=False)
        if result:
            return result['data_value']
        else:
            return defValue

    def gets(self, keys: (list, set), limit: int = 0) -> dict:
        from dber import inSql
        sql = f"SELECT data_key,data_value FROM {self.__tableName()} WHERE data_key {inSql(keys)}"
        rows = self.db.select(sql, limit=limit, hump=False)
        kv = {}
        if rows:
            for row in rows:
                kv[row['data_key']] = row['data_value']
        return kv

    def getFile(self, key: str, file: str = None):
        fileBytes = self.get(key)
        if fileBytes:
            if file:
                import os
                filedir = os.path.abspath(os.path.dirname(file))
                if not os.path.exists(filedir) or not os.path.isdir(filedir):
                    os.makedirs(filedir)
                with open(file, 'wb+') as f:
                    f.write(fileBytes)
                    f.flush()
                    f.close()
            return fileBytes

    def getRandoms(self, limit: int = 10) -> dict:
        return self.gets(self.randomKeys(limit), limit)

    def like(self, likeKey: str, limit: int = 0) -> dict:
        sql = f"SELECT data_key,data_value FROM {self.__tableName()} WHERE data_key like '{likeKey}'"
        rows = self.db.select(sql, limit=limit, hump=False)
        kv = {}
        if rows:
            for row in rows:
                kv[row['data_key']] = row['data_value']
        return kv

    def remove(self, key: str):
        sql = f"DELETE FROM {self.__tableName()} WHERE data_key = ?"
        self.db.delete(sql, key)

    def removes(self, keys: (list, tuple, set)):
        from dber import inSql
        sql = f"DELETE FROM {self.__tableName()} WHERE data_key {inSql(keys)}"
        self.db.delete(sql)

    def clear(self):
        self.db.drop(self.__tableName())

    def size(self):
        return self.db.count(self.__tableName())

    def contains(self, key: str) -> bool:
        return self.db.count(self.__tableName(), f"data_key = '{key}'") > 0

    def getFloat(self, key: str, defValue: (int, float) = None) -> float:
        value = self.get(key, defValue)
        if value:
            return float(value)

    def getInt(self, key: str, defValue: (int, float) = None) -> int:
        value = self.getFloat(key, defValue)
        if value:
            return int(value)

    def getBool(self, key: str, defValue: bool = None) -> bool:
        value = self.get(key, defValue)
        if value:
            if isinstance(value, str):
                if value in ('False', 'false', '0'):
                    return False
                if value in ('True', 'true', '1'):
                    return True
                raise ValueError("转换bool类型失败：result={0} , 实际类型：{1}".format(value, type(value)))
            if isinstance(value, (int, bool, float)):
                return bool(value)
            raise ValueError("转换bool类型失败：result={0} , 实际类型：{1}".format(value, type(value)))

    def getString(self, key: str, defValue=None) -> str:
        value = self.get(key, defValue)
        if value:
            return str(value)

    def getList(self, key: str, defValue: (str, list, set) = None, splitChar: str = ',') -> list:
        value = self.get(key)
        if not value:
            return list(defValue or [])
        if isinstance(value, bytes):
            return [value]
        import json
        try:
            listObject = json.loads(value)
            if isinstance(listObject, list):
                return listObject
        except json.decoder.JSONDecodeError:
            if isinstance(value, str):
                return value.split(splitChar)
        raise ValueError("转换list类型失败：result={0} , 实际类型：{1}".format(value, type(value)))

    def getSet(self, key: str, defValue: (str, list, set) = None, splitChar: str = ',') -> set:
        listValue = self.getList(key, defValue, splitChar)
        if listValue:
            return set(listValue)

    def getDict(self, key: str, defValue: (dict, tuple) = None) -> dict:
        value = self.getJson(key)
        if not value:
            return dict(defValue or {})
        if isinstance(value, dict):
            return value
        else:
            raise ValueError("转换dict类型失败：result={0} , 实际类型：{1}".format(value, type(value)))

    def getJson(self, key: str):
        value = self.get(key)
        if value:
            if isinstance(value, bytes):
                raise ValueError("转换dict类型失败：result={0} , 实际类型：{1}".format(value, type(value)))
            import json
            return json.loads(value)

    def close(self):
        self.db.close()

    def __del__(self):
        self.close()


class ShelveMapDB(MapDB):
    pass


class SQLiteMapDB(MapDB):

    def __init__(self, database='sqlitemap.db', topic='default', debug: bool = False, inner=False):
        from dber import SQLite
        if inner:
            import os
            database = os.path.join(os.path.expanduser('~'), "sqlitemap.db")
        db = SQLite(database=database, debug=debug)
        super().__init__(db, topic)


class MySQLMapDB(MapDB):

    def __init__(self, topic='default', host="localhost", port: int = 3306, username="root", password="",
                 database="test", charset: str = "utf8mb4", debug: bool = False, **config):
        from dber import MySQL
        db = MySQL(host=host, port=port, username=username, password=password, database=database,
                   charset=charset,
                   debug=debug,
                   **config)
        super().__init__(db, topic)

    def randomKeys(self, limit: int = 10) -> list:
        rows = self.db.selectTable(self._MapDB__tableName(), "data_key", where="1=1 order by rand()", limit=limit)
        keys = []
        if rows:
            for row in rows:
                keys.append(row['data_key'])
        return keys

    def like(self, likeKey: str, limit: int = 0) -> dict:
        if likeKey.__contains__("%"):
            likeKey = likeKey.replace("%", "%%")
        sql = f"SELECT data_key,data_value FROM {self._MapDB__tableName()} WHERE data_key like '{likeKey}'"
        rows = self.db.select(sql, limit=limit, hump=False)
        kv = {}
        if rows:
            for row in rows:
                kv[row['data_key']] = row['data_value']
        return kv


__db = SQLiteMapDB(inner=True)


def get(key: str = None, defValue=None):
    if key:
        return __db.get(key, defValue)
    else:
        return __db


def gets(keys: (list, set), limit: int = 0) -> dict:
    return get().gets(keys, limit=limit)


def getFile(key: str, file: str = None):
    return get().getFile(key, file)


def put(key: str, value):
    return get().put(key, value)


def puts(key: str, kv_items: dict):
    return get().puts(key, kv_items)


def putBytes(key: str, byteArrays: bytes):
    return get().putBytes(key, byteArrays)


def putFile(key: str, filePath: str):
    return get().putFile(key, filePath)


def remove(key: str):
    return get().remove(key)


def removes(keys: (list, tuple, set)):
    return get().removes(keys)


def clear():
    return get().clear()


def keys(limit: int = 0) -> list:
    return get().keys(limit=limit)


def size():
    return get().size()


def like(likeKey: str, limit: int = 0) -> dict:
    return get().like(likeKey, limit=limit)


def contains(key: str) -> bool:
    return get().contains(key)


def enableDebug():
    get().enableDebug()


def disableDebug():
    get().disableDebug()
