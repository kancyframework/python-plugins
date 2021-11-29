### [Python 下划线和双下划线的作用](https://www.cnblogs.com/hls-code/p/14777980.html)
```text
_xxx与__xxx与__xxx__的区别
xx: 公有变量
_x: 单前置下划线,私有化属性或方法，禁止通过from modules import *导入,但是类对象和子类可以访问
__xx：双前置下划线,避免与子类中的属性命名冲突，无法在外部直接访问(名字重整所以访问不到)，类对象和子类不能访问
__xx__:双前后下划线,用户名字空间的魔法对象或属性。例如:__init__ , __ 尽量不要自定义这种形式的。
xx_:单后置下划线,用于避免与Python关键词的冲突

其实__方式的私有属性不可访问的原理很简单，当你在类中定义一个变量为私有变量时，python自动会将此属性名字改掉；
在类的外部使用__dict__显示一个实例所有属性，可以发现name被改成了_类名__私有属性名，所以在字典中访问私有属性名报错
```


### Gui开发手册
[wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder/releases)
```cmd
pip install wxPython
```
