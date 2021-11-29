import datetime
import decimal


class A(object):

    def __init__(self) -> None:
        self.name = 'string'
        self.age = 18
        self.score = decimal.Decimal('85.5')
        self.love = {'apple', 'cat', 'dog'}
        self.logs = ['日志1', '日志2']


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


import langeer

print(langeer.obj2dict(C()))

