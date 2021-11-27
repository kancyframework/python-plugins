import time

from typing import Iterable


def inSql(*items):
    """
    拼接in查询Sql语句
    :param items: in条件的元素
    :return: "in (1,2,3) "
    """
    if not items or items.__sizeof__() < 1:
        raise RuntimeError("in items is empty.")
    realItems = []
    for it in items:
        if isinstance(it, bool):
            raise ValueError(f"in item value type is not support : {type(it)}")
        elif isinstance(it, (str, int, float)):
            realItems.append(it)
        elif isinstance(it, (list, tuple, set)):
            realItems.extend(it)
        else:
            raise ValueError(f"in item value type is not support : {type(it)}")
    del items
    realItems = set(realItems)
    sqlItems = []
    for item in realItems:
        if isinstance(item, (int, float)):
            sqlItems.append(str(item))
        else:
            sqlItems.append(f"\"{item}\"")
    return f" in ({','.join(sqlItems)}) "


class DB(object):
    """
    数据库基类
    """

    def __init__(self, connection, dbType: str = None,
                 debug: bool = False) -> None:
        self.__closed = False
        self.__debug = debug
        self.__dbType = dbType
        self.__connection = connection
        self.select("select 1")

    def select(self, sql, *parameters, limit: int = 0, hump: bool = True, **kwargs) -> list[dict]:
        """
        查询数据
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param limit: 结果限制
        :param hump: 转驼峰
        :param kwargs: 其他属性
        :return: 字典列表
        """
        st = time.time()
        sql = self.__sql(sql)
        parameters = self.__parameters(*parameters)
        cursor = self.getConnection().cursor()
        try:
            if limit < 1:
                cursor.execute(sql, parameters, **kwargs)
                dataRows = list(cursor.fetchall())
            else:
                if not sql.__contains__(" limit ") and not sql.__contains__(" LIMIT "):
                    if sql.__contains__(";"):
                        sql = sql.replace(";", f" limit {limit};")
                    else:
                        sql = f"{sql} limit {limit}"
                cursor.execute(sql, parameters, **kwargs)
                dataRows = cursor.fetchmany(limit)
            if hump and dataRows:
                for i in range(0, len(dataRows)):
                    dataRows[i] = self.__humpRow(dataRows[i])
                return dataRows
            return dataRows
        finally:
            self.__printSql(sql, parameters, st)
            cursor.close()

    def selectOne(self, sql, *parameters, hump: bool = True) -> dict:
        """
        查询一行数据
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param hump: 转驼峰
        :return: 数据行字典
        """
        st = time.time()
        sql = self.__sql(sql)
        parameters = self.__parameters(*parameters)
        cursor = self.getConnection().cursor()
        try:
            cursor.execute(sql, parameters)
            result = cursor.fetchone()
            if result:
                row = dict(result)
                if not hump:
                    return row
                return self.__humpRow(row)
        finally:
            self.__printSql(sql, parameters, st)
            cursor.close()

    def selectTable(self, table, columns: str = "*", where: str = "1 = 1", limit: int = 0, hump: bool = True,
                    **conditions):
        """
        查询数据
        :param table: 表名
        :param columns: 查询的字段，默认所有字段
        :param where: where条件
        :param limit: 返回数据行限制
        :param hump: 是否转驼峰
        :param conditions: where条件
        :return: 列表字典
        """
        if not (where.__contains__("where ") or where.__contains__("WHERE ")):
            where = f"where {where}"
        sql = ""
        sql += f"select {columns} from {table} {where}"
        for key in conditions.keys():
            value = conditions[key]
            if isinstance(value, (int, float)):
                sql += f" and {key} = {conditions[key]}"
            else:
                sql += f" and {key} = '{conditions[key]}'"
        return self.select(sql, (), limit=limit, hump=hump)

    def callbackResultSet(self, sql, *parameters, callback=None, **kwargs):
        """
        回调处理查询结果集
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param callback: 回调函数 fun(row)
        :param kwargs: 其他配置
        :return:
        """
        if not callback:
            raise RuntimeError("callback fun not found")
        st = time.time()
        sql = self.__sql(sql)
        parameters = self.__parameters(*parameters)
        cursor = self.getConnection().cursor()
        try:
            cursor.execute(sql, parameters, **kwargs)
            while True:
                try:
                    row = cursor.__next__()
                    callback(self.__humpRow(row))
                except StopIteration:
                    break
        finally:
            self.__printSql(sql, parameters, st)
            cursor.close()

    def execute(self, sql, *parameters, commit=True, **kwargs):
        """
        执行SQL
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        st = time.time()
        sql = self.__sql(sql)
        parameters = self.__parameters(*parameters)
        cursor = self.getConnection().cursor()
        try:
            cursor.execute(sql, parameters, **kwargs)
            if commit or commit > 0:
                self.commit()
        finally:
            self.__printSql(sql, parameters, st)
            cursor.close()

    def update(self, sql, *parameters, commit=True, **kwargs):
        """
        更新数据
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        self.execute(sql, *parameters, commit=commit, **kwargs)

    def insert(self, sql, *parameters, commit=True, **kwargs):
        """
        插入数据
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        return self.execute(sql, *parameters, commit=commit, **kwargs)

    def insertBatch(self, sql, rows: Iterable[Iterable], commit=True, **kwargs):
        """
        批量插入
        :param sql: SQL语句
        :param rows: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        st = time.time()
        sql = self.__sql(sql)
        cursor = self.__connection.cursor()
        try:
            cursor.executemany(sql, rows, **kwargs)
            if commit or commit > 0:
                self.commit()
        finally:
            self.__printSql(sql, rows, st)
            cursor.close()

    def replace(self, sql, *parameters, commit=True, **kwargs):
        """
        替换数据（插入或按唯一键更新）
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        return self.execute(sql, *parameters, commit=commit, **kwargs)

    def replaceBatch(self, sql, rows: Iterable[Iterable], commit=True, **kwargs):
        """
        批量插入
        :param sql: SQL语句
        :param rows: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        return self.insertBatch(sql, rows, commit, **kwargs)

    def delete(self, sql, *parameters, commit=True, **kwargs):
        """
        删除数据
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param commit: 是否自动提交
        :param kwargs: 其他配置
        :return:
        """
        return self.execute(sql, *parameters, commit=commit, **kwargs)

    def clear(self, table, commit=True, **kwargs):
        """
        清空表数据
        :param table: 表名
        :param commit: 自动提交
        :param kwargs: 其他配置
        :return:
        """
        if self.__dbType == 'mysql':
            self.execute(f"TRUNCATE TABLE {table}", commit=commit, **kwargs)
        else:
            self.execute(f"DELETE FROM {table}", commit=commit, **kwargs)

    def drop(self, table, commit=True, **kwargs):
        """
        删除表
        :param table: 表名
        :param commit: 自动提交
        :param kwargs: 其他配置
        :return:
        """
        self.execute(f"DROP TABLE IF EXISTS {table}", commit=commit, **kwargs)

    def count(self, table, where: str = None):
        """
        统计表的行数
        :param table: 表名
        :param where: 额外条件
        :return: 其他配置
        """
        sql = f"SELECT COUNT(1) AS cnt FROM {table}"
        if where and len(where) > 0:
            if not (where.__contains__("where ") or where.__contains__("WHERE ")):
                sql = f"{sql} WHERE {where}"
            else:
                sql = f"{sql} {where}"
        return self.getColumnIntValue(sql, defValue=0)

    def getColumnValue(self, sql, *parameters, column: str = None, defValue=None):
        """
        查询字段的值
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param column: 查询的字段值
        :param defValue: 默认值
        :return:
        """
        if column and len(column) > 0:
            row = self.selectOne(sql, *parameters)
            if row and row.__contains__(column):
                return row[column]
        else:
            row = self.selectOne(sql, *parameters, hump=False)
            if row and len(row) == 1:
                for cn in row:
                    return row[cn]
            else:
                raise RuntimeError(f"There are multiple columns, but did not specify the only one : {set(row.keys())}")
        return defValue

    def getColumnFloatValue(self, sql, *parameters, column: str = None, defValue: float = None) -> float:
        """
        查询字段的值
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param column: 查询的字段值
        :param defValue: 默认值
        :return:
        """
        value = self.getColumnValue(sql, *parameters, column=column, defValue=defValue)
        if value:
            return float(value)

    def getColumnBoolValue(self, sql, *parameters, column: str = None, defValue: bool = None) -> bool:
        """
        查询字段的值
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param column: 查询的字段值
        :param defValue: 默认值
        :return:
        """
        value = self.getColumnValue(sql, *parameters, column=column, defValue=defValue)
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

    def getColumnIntValue(self, sql, *parameters, column: str = None, defValue: int = None) -> int:
        """
        查询字段的值
        :param sql: SQL语句
        :param parameters: SQL占位符参数
        :param column: 查询的字段值
        :param defValue: 默认值
        :return:
        """
        value = self.getColumnFloatValue(sql, *parameters, column=column, defValue=defValue)
        if value:
            return int(value)

    def callProc(self, procName: str, args):
        """
        调用存储过程
        :param procName: 存储过程名称
        :param args: 存储过程参数
        :return:
        """
        st = time.time()
        cursor = self.getConnection().cursor()
        try:
            cursor.callproc(procName, args)
        finally:
            self.__printSql(f"call proc : {procName}, args: {args}", st)
            cursor.close()

    def getConnection(self):
        """
        连接是否关闭
        :return:
        """
        if self.isClosed():
            raise RuntimeError("Database connection is closed")
        return self.__connection

    def commit(self):
        """
        提交事务
        :return:
        """
        if not self.isClosed():
            self.__connection.commit()

    def rollback(self):
        """
        回滚事务
        :return:
        """
        if not self.isClosed():
            self.__connection.rollback()

    def isClosed(self) -> bool:
        """
        连接是否关闭
        :return:
        """
        return self.__closed

    def close(self):
        """
        关闭连接
        :return:
        """
        if not self.isClosed():
            self.commit()
            self.__connection.close()
            self.__closed = True
            if self.__debug:
                print(f"成功关闭DB：{self}, close conn: {self.__connection}")

    def enableDebug(self):
        """
        启用debug能力
        :return:
        """
        self.__debug = True

    def disableDebug(self):
        """
         禁止debug能力
         :return:
         """
        self.__debug = False

    def getDatabaseType(self):
        """
        获取数据库类型
        :return:
        """
        return self.__dbType

    def __printSql(self, sql, params, st):
        """
        打印执行的SQL语句
        :param sql: 执行SQL
        :param st: 开始处理的时间
        :return:
        """
        if sql and self.__debug:
            ct = (time.time() - st)
            if ct > 1:
                ct = f"{round(ct, 3)}s"
            else:
                ct = f"{round(ct * 1000, 3)}ms"
            if params:
                print(f"===> ExecuteSQL[{ct}]: {sql} ， params : {params}")
            else:
                print(f"===> ExecuteSQL[{ct}]: {sql}")

    def __parameters(self, *parameters):
        params = []
        if parameters:
            for param in parameters:
                if not param:
                    continue
                if isinstance(param, bool):
                    raise ValueError(f"sql parameters value type is not support : {type(param)}")
                elif isinstance(param, (str, int, float)):
                    params.append(param)
                elif isinstance(param, (list, tuple, set)):
                    params.extend(param)
                else:
                    raise ValueError(f"sql parameters value type is not support : {type(param)}")
        return params

    def __sql(self, sql) -> str:
        if self.__dbType == 'mysql':
            sql = sql.replace("?", "%s")
        elif self.__dbType == 'sqlite':
            sql = sql.replace("%s", "?").replace("%d", "?")
        else:
            sql = sql
        return sql

    def __del__(self):
        self.close()
        del self.__connection

    @staticmethod
    def __str2Hump(columnName):
        arr = filter(None, columnName.lower().split('_'))
        res = ''
        for item in arr:
            res = res + item[0].upper() + item[1:]
        res = res[0].lower() + res[1:]
        return res

    @staticmethod
    def __humpRow(row) -> dict:
        if row:
            newRow = dict(row)
            for key in row.keys():
                newRow[DB.__str2Hump(key)] = row[key]
            return newRow


class SQLite(DB):
    def __init__(self, database, debug: bool = False) -> None:
        """
        SQLite3数据库
        :param database:
        :param debug:
        """
        import sqlite3
        self.__database = database
        self.__debug = debug
        self.__connection = sqlite3.connect(database)
        self.__connection.row_factory = self.__dict_factory
        super().__init__(self.__connection, debug=self.__debug, dbType='sqlite')

    def executeScript(self, sqlScript: str, commit=True):
        """
        执行SQL脚本
        :param sqlScript: sql脚本
        :param commit: 自动提交
        :return:
        """
        st = time.time()
        cursor = self.getConnection().cursor()
        try:
            cursor.executescript(sqlScript)
            if commit or commit > 0:
                self.commit()
        finally:
            self._DB__printSql(sqlScript, None, st)
            cursor.close()

    def executeScriptFile(self, sqlScriptFilePath: str, commit=True):
        """
        执行SQL脚本文件
        :param sqlScriptFilePath: sql脚本文件路径
        :param commit: 自动提交
        :return:
        """
        import os
        if os.path.exists(sqlScriptFilePath) and os.path.isfile(sqlScriptFilePath):
            with open(sqlScriptFilePath, 'r') as f:
                sqlScript = f.read()
            if sqlScript and len(sqlScript) > 0:
                self.executeScript(sqlScript, commit)

    def getBusinessDatabaseNames(self) -> list[str]:
        """
        获取业务数据库名称
        :return:
        """
        return self.getDatabaseNames()

    def getDatabaseNames(self) -> list[str]:
        """
         获取所有数据库名称
         :return:
         """
        return ["main"]

    def getTables(self, tables=None) -> list[dict]:
        return self.select("select distinct tbl_name as table_name, sql from sqlite_master "
                           f"where type = 'table' and tbl_name {inSql(tables)}")

    def getTableNames(self) -> list[str]:
        """
        获取所有数据库名称
        :return:
        """
        rows = self.select("select distinct tbl_name from sqlite_master where type = 'table'", hump=False)
        databaseNames = []
        if rows:
            for row in rows:
                databaseNames.append(row['tbl_name'])
        return databaseNames

    @staticmethod
    def __dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class MySQL(DB):
    """
    Mysql数据库
    """

    def __init__(self, host="localhost", port: int = 3306, username="root", password="", database="information_schema",
                 charset: str = "utf8mb4",
                 debug: bool = False,
                 **config) -> None:
        import pymysql
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__charset = charset
        self.__debug = debug
        self.__connection = pymysql.connect(host=host, port=port, user=username, password=password, database=database,
                                            charset=charset, cursorclass=pymysql.cursors.DictCursor, **config)
        super().__init__(self.__connection, debug=self.__debug, dbType='mysql')

    def setDatabase(self, database: str):
        self.__connection.select_db(database)
        self.__database = database or self.__database

    def getBusinessDatabaseNames(self) -> list[str]:
        """
        获取业务数据库名称
        :return:
        """
        databaseNames = self.getDatabaseNames()
        if databaseNames:
            databaseNames.remove("information_schema")
            databaseNames.remove("performance_schema")
            databaseNames.remove("test")
            databaseNames.remove("mysql")
            databaseNames.remove("sys")
        return databaseNames

    def getDatabaseNames(self) -> list[str]:
        """
        获取所有数据库名称
        :return:
        """
        rows = self.select("select distinct table_schema from information_schema.tables", hump=False)
        databaseNames = []
        if rows:
            for row in rows:
                databaseNames.append(row['table_schema'])
        return databaseNames

    def getTables(self, database: str = None) -> list[dict]:
        """
        获取数据库下所有表信息
        :param database: 数据库名，默认为连接的数据库
        :return:
        """
        if not database:
            database = self.__database
        return self.select(
            "select table_name,table_comment,create_time,update_time,table_rows,data_length,index_length,auto_increment "
            "from information_schema.tables "
            f"where table_schema = '{database}'")

    def getTableNames(self, database: str = None, lower=True) -> list[str]:
        """
        获取数据库下所有表名称
        :param database: 数据库名，默认为连接的数据库
        :param lower: 表明是否小写
        :return:
        """
        if not database:
            database = self.__database
        tableInfos = self.select(
            f"select table_name from information_schema.tables where table_schema = '{database}'", hump=False)
        tableNames = []
        if tableInfos:
            for tableInfo in tableInfos:
                tb = tableInfo['table_name']
                tableNames.append(lower and tb.lower() or tb)
        return tableNames

    def getTableColumns(self, table: str, database: str = None) -> list[str]:
        """
        获取表的字段信息
        :param table: 表名
        :param database: 数据库名，默认为连接的数据库
        :return:
            column_name     字段名称 ： username
            data_type       字段数据类型： varchar
            column_type     字段类型 ： varchar(40)
            is_nullable     是否为空 ： YES/NO
            column_key      索引类型 ： PRI/UNI/MUL (主键索引/唯一索引/普通索引)
            column_comment  字段注释： 用户名称
            column_default  默认值 ：CURRENT_TIMESTAMP/其他
                    extra ：扩展信息
                                on update CURRENT_TIMESTAMP
                                auto_increment
        """
        if database:
            database = self.__database
        return self.select(
            f"select column_name,data_type,column_type,is_nullable,column_key,column_comment,column_default,extra "
            "from INFORMATION_SCHEMA.COLUMNS "
            f"where table_schema = '{database}' and table_name = '{table}' "
            "order by ordinal_position")

    def getColumnInfo(self, table: str, column: str, database: str = None):
        """
        获取表字段信息
        :param table: 表名
        :param column: 字段名
        :param database: 数据库名，默认为连接的数据库
        :return:
            column_name     字段名称 ： username
            data_type       字段数据类型： varchar
            column_type     字段类型 ： varchar(40)
            is_nullable     是否为空 ： YES/NO
            column_key      索引类型 ： PRI/UNI/MUL (主键索引/唯一索引/普通索引)
            column_comment  字段注释： 用户名称
            column_default  默认值 ：CURRENT_TIMESTAMP/其他
                    extra ：扩展信息
                                on update CURRENT_TIMESTAMP
                                auto_increment
        """
        if database:
            database = self.__database
        return self.selectOne(
            f"select column_name,data_type,column_type,is_nullable,column_key,column_comment,column_default,extra "
            "from INFORMATION_SCHEMA.COLUMNS "
            f"where table_schema = '{database}' and table_name = '{table}' and column_name= '{column}' "
            "order by ordinal_position")
