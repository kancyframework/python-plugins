import os
from dber.dber import MySQL
from dber.dber import SQLite

database = "test.db"

rows = []
for i in range(0, 100):
    rows.append((f"k{i}", f"v{i}"))

db = SQLite(database, debug=True)
# db = MySQL(password="root", database="test", debug=True)
db.execute("CREATE TABLE IF NOT EXISTS t_test (data_key varchar(255) PRIMARY KEY, data_value text);")
print(db.getTableNames())
print(db.insertBatch("replace into t_test values(%s,?)", rows))
print(db.replace("replace into t_test values(%s,%s)", ('kancy', '25')))
print(db.selectTable("t_test", "data_value", data_key='kancy'))
print(db.selectTable("t_test", "data_value", where='data_key="kancy"'))
print(db.select("select data_key from t_test where data_key in (?,?)", "k1", "k2"))
print(db.select("select data_key from t_test where data_key in (?,?)", ("k1", "k2")))
print(db.select("select data_key from t_test where data_key in (?,?)", ["k1", "k2"], hump=False))
print(db.select("select data_key from t_test where data_key in (?,?)", ["k1"], ["k2"]))
print(db.select("select data_key from t_test where data_key in (?,?)", ["k1"], "k2"))
print(db.select("select data_key from t_test", limit=3))
print(db.selectOne("select data_key from t_test"))
print(db.update("update t_test set data_value = ? where data_key = ?", 100, 'k0'))
print(db.selectOne("select data_value from t_test"))
print(db.getColumnIntValue("select data_value from t_test where data_key = ?", 'k0'))
print(db.getColumnFloatValue("select data_key,data_value from t_test where data_key = ?", 'k0', column="data_value"))
print(db.update("update t_test set data_value = ? where data_key = ?", '0', 'k1'))
print(db.getColumnBoolValue("select data_value from t_test where data_key = ?", 'k1', column="data_value"))
print(db.getColumnIntValue("select count(1) as cnt from t_test"))
print(db.delete("delete from t_test"))
print(db.selectOne("select data_value from t_test"))
db.close()

if os.path.exists(database) and os.path.isfile(database):
    os.remove(database)
