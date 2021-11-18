import configparser


class Confer:

    def __init__(self, filePath: str, encoding="utf-8") -> None:
        self.filePath = filePath
        self.encoding = encoding
        self.config = configparser.ConfigParser()
        self.config.read(filePath, encoding)

    def get(self, section, key):
        if self.config.has_option(section, key):
            return self.config.get(section, key)

    def get(self, section, key, defValue=None):
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return defValue

    def getInt(self, section, key, defValue: int = None) -> int:
        if self.config.has_option(section, key):
            return self.config.getint(section, key)
        return defValue

    def getFloat(self, section, key, defValue: float = None) -> float:
        if self.config.has_option(section, key):
            return self.config.getfloat(section, key)
        return defValue

    def getBoolean(self, section, key, defValue: bool = None) -> bool:
        if self.config.has_option(section, key):
            return self.config.getboolean(section, key)
        return defValue

    def getJson(self, section, key, defValue=None):
        if self.config.has_option(section, key):
            value = self.config.get(section, key)
            if value:
                import json
                return json.loads(value)
        return defValue

    def getList(self, section, key, defValue: (set, list, tuple) = None) -> list:
        listValue = self.getJson(section, key, defValue)
        if listValue:
            return list(listValue)

    def getSet(self, section, key, defValue: (set, list, tuple) = None) -> set:
        listValue = self.getJson(section, key, defValue)
        if listValue:
            return set(listValue)

    def getDict(self, section, key, defValue: dict = None) -> dict:
        return self.getJson(section, key, defValue)

    def set(self, section, key, value, autoCommit: bool = True):
        if not self.config.has_section(section):
            self.config.add_section(section)
        realValue = value
        if isinstance(value, (str, int, bool, float)):
            realValue = str(value)
        else:
            import json
            realValue = json.dumps(realValue)
        self.config.set(section, key, realValue)
        if autoCommit:
            self.save()

    def contains(self, section, key=None) -> bool:
        return self.has(section, key)

    def has(self, section, key=None) -> bool:
        if not self.config.has_section(section):
            return False
        if key:
            return self.config.has_option(section, key)
        return True

    def remove(self, section, key=None, autoCommit: bool = True):
        if not self.config.has_section(section):
            return
        if key:
            self.config.remove_option(section, key)
        else:
            self.config.remove_section(section)
        if autoCommit:
            self.save()

    def clear(self):
        sections = self.config.sections()
        if sections:
            for section in sections:
                self.config.remove_section(section)
            self.save()

    def save(self):
        self.config.write(open(self.filePath, 'w'))

    def refresh(self):
        self.config.read(self.filePath, self.encoding)
