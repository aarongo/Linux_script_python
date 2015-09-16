# _*_coding:utf-8_*_
# __author__ = 'yulong'
# DATE:'15-9-14'

# msyql 链接基类
# select d.id from milieu_group d where d.milieu='carrefour';
# select t.password  from user_info t,milieu_group d where d.id=t.milieu_id and d.milieu='B2B2c';
# select  t.name from user_info t,milieu_group d where d.id=t.milieu_id and d.milieu='B2B2c';

import MySQLdb
from conf import mysql_config


class DB(object):
    def __init__(self):
        self.__conn = MySQLdb.connect(host=mysql_config.DATABASE['host'],
                                      port=mysql_config.DATABASE['port'],
                                      user=mysql_config.DATABASE['username'],
                                      passwd=mysql_config.DATABASE['password'],
                                      db=mysql_config.DATABASE['db_name'])
        self.__cursor = self.__conn.cursor()

    def query(self, sqltxt):
        self.__cursor.execute(sqltxt)
        res = self.__cursor.fetchall()
        return res

    def inster(self, sqltxt):
        self.__cursor.execute(sqltxt)
        self.__conn.commit()
        self.__cursor.close()
        self.__conn.close()
