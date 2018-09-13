# -*- coding: UTF-8 -*-
"""
1、执行带参数的ＳＱＬ时，请先用sql语句指定需要输入的条件列表，然后再用tuple/list进行条件批配
２、在格式ＳＱＬ中不需要使用引号指定数据类型，系统会根据输入参数自动识别
３、在输入的值中不需要使用转意函数，系统会自动处理
"""

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
# from PooledDB import PooledDB
import conf.path_config as Config

""" 
Config是一些数据库的配置文件 
"""


class Mysql(object):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, params=None):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        if params:
            if Mysql.__pool is None:
                __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                                  host=params.get('host'), port=params.get('port'), user=params.get('username'),
                                  passwd=params.get('pwd'),
                                  db=params.get('dbname'), use_unicode=False, charset='utf8', cursorclass=DictCursor)
            self._conn = __pool.connection()
        else:
            self._conn = Mysql.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if Mysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                              host=Config.DBHOST, port=Config.DBPORT, user=Config.DBUSER, passwd=Config.DBPWD,
                              db=Config.DBNAME, use_unicode=False, charset=Config.DBCHAR, cursorclass=DictCursor)
        return __pool.connection()

    def getAll(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchall()
        else:
            result = []

        return result

    def getOne(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchone()
        else:
            result = False
        return result

    def getMany(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        if count > 0:
            result = self._cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertOne(self, sql, value):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        self._cursor.execute(sql, value)
        return self.__getInsertId()


    def insertMany(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = self._cursor.executemany(sql, values)
        return count

    def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cursor.execute("SELECT @@IDENTITY AS id")
        result = self._cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        if param is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, param)
        return count

    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def execute(self, sql):
        """
        @summary: 执行纯字符串sql
        @param sql: ＳＱＬ格式及条件
        @return: None
        """
        return self.__query(sql, None)

    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()


if __name__ == '__main__':
    mysql = Mysql()
    id = '50967'
    rows = mysql.getAll("select *  from QUESTION_AUTO where id = %s" % id)
    print(type(rows))
    # print(rows)
    # sql = "INSERT INTO chat_message (type,content_type, emotion_score, negative_score, positive_score) VALUES(%(type)s, %(content_type)s, %(emotion_score)s, %(negative_score)s, %(positive_score)s)"
    # value = { 1, 4, 5.0, -2.0, 5.0}
    # value = {"type": 1, "content_type": 4, "emotion_score": 5.0, "negative_score": -2.0, "positive_score": 5.0}
    # print(mysql.insertOne(sql, value))
    # mysql.commit()
    # insertsql = "insert into chat_message (type,content_type,emotion_score,negative_score,positive_score) values (1,'信用卡如何办理',5.0,4.0,-2.0)"
    # chat_message = "xyz"
    # mysql.insertOne(insertsql)
    # # myid = 501
    # currentnodesql = 'select * from ENGINE_NODE_INFO where id =:myid'
    # row1 = ora.getAll(currentnodesql,{'myid':myid})
    # print(row1)
