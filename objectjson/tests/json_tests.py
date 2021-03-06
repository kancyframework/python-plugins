import datetime
import decimal
import objectjson


class A(object):

    def __init__(self) -> None:
        self.name = 'string'
        self.age = 18
        self.score = decimal.Decimal('85.5')
        self.love = {'apple', 'cat', 'dog'}
        self.logs = ['日志1', '日志2']
        self.bytedata = b"hello"


class B(A):

    def __init__(self) -> None:
        super().__init__()
        self.a = A()
        self.date = datetime.datetime.now()
        self.datetime = datetime.date.today()


class C(object):

    def __init__(self) -> None:
        self.a = A()
        self.b = B()


print(objectjson.toJsonString(C()))
a = objectjson.jsondumps(objectjson.toJsonString(C()))
print(objectjson.toJson(objectjson.readJsonString(objectjson.toJsonString(C())), True))
