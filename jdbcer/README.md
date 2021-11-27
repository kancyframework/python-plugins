
### 使用教程

**快速开始**

```python
import jdbcer

db = jdbcer.SQLite("test.db")

create_table_sql = """
    CREATE TABLE IF NOT EXISTS t_test (
        data_key varchar(255) PRIMARY KEY, 
        data_value text,
        data_int integer
    );
"""
# 创建数据表
db.execute(create_table_sql)

# 插入数据
db.replace("replace into t_test values (?,?,?)", "test_key", "test_data", 1)

# 查询数据
print(db.select("select * from t_test where data_key = ?", "test_key"))
print(db.selectOne("select * from t_test where data_key = ?", "test_key"))
print(db.selectTable("t_test", data_key="test_key"))

# 查询字段
print(db.getColumnIntValue("select data_int from t_test where data_key = ?", "test_key"))
print(db.getColumnFloatValue("select data_int from t_test where data_key = ?", "test_key"))
print(db.getColumnBoolValue("select data_value,data_int from t_test where data_key = ?", "test_key", column="data_int"))

# 批量插入数据
rows = []
for i in range(0, 100):
    row = (f"k{i}", f"v{i}", i)
    rows.append(row)

db.replaceBatch("replace into t_test values (?,?,?)", rows)
print(db.count("t_test"))
print(db.count("t_test", where="data_int > 90"))

# 更新数据
db.update("update t_test set data_int=? where data_key = ?", 100, 'test_key')

# 删除数据
db.delete("delete from t_test")
# 清空表
db.clear("t_test")
# 删除表
db.drop("t_test")

# 关闭
db.close()
```