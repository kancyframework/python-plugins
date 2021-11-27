### 使用手册

**快速开始**
```python
import mapdb

# default map db file : {userHome}/sqlitemap.db

# 写普通属性
mapdb.put("int", 20)
mapdb.put("float", 1.75)
mapdb.put("bool", False)
mapdb.put("string", 'kancy')
mapdb.put("hobby", ["play games"])
mapdb.putBytes("bytes", b"I am bytearray.")

print(mapdb.gets(['int', 'float', 'bool', 'string', 'hobby', 'bytes']))

# 写json
json = {
    "name":"kancy",
    "age":20,
    "height":1.75,
    "hobby":["play games"],
    "map":{
        "k":"v"
    }
}
mapdb.put("json", json)
print(mapdb.get("json"))
print(mapdb.get().getJson("json"))

# 写文件
mapdb.putFile("textfile", "data/text.txt")
mapdb.putFile("imgfile", "data/img.png")
mapdb.getFile("textfile", "data/text.txt")
mapdb.getFile("imgfile", "data/img.png")
```

**自定义MapDB**
```python
import mapdb

# SQLite实现
db1 = mapdb.SQLiteMapDB(debug=True)

# MySQL实现
db2 = mapdb.MySQLMapDB(host="localhost", username="root", password="root")
```

