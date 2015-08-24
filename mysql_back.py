# _*_coding:utf-8_*_
'''Author       lonnyliu
    Use Of      Linux backup file
    Time        2015-08-17
    Email       lonnyliu@126.com
    Introduction mysql backup and delete three days ago
'''
import datetime
import subprocess


# 定义删除几天前的备份
day = 3
# 获取时间戳
now = datetime.datetime.now().strftime("%Y-%m-%d-%H")
back_dir = "/install/back/"
command = "/install/mysql/bin/mysqldump -uroot -pcomall2014 cybershop_test > cybershop_test@%s%s.sql" % (back_dir, now)
command_delete = "find %s -mtime +%s -delete" % (back_dir, day)


class Mysql(object):
    def __init__(self, command, command_delete):
        self.command = command
        self.command_delete = command_delete

    def backup(self):
        # 定义命令执行变量
        com = subprocess.Popen(command, shell=True)
        # 等待命令执行完成
        print "Running programs.............."
        com.wait()
        if com.returncode == 0:
            print "----------数据库备份成功----------"
            print "----------检测备份文件，删除3天前的备份----------"
            print "--------Runing com_delete----------"
            com_delete = subprocess.Popen(command_delete, shell=True)
            com_delete.wait()
            if com_delete == 0:
                print "----------删除3天前备份成功----------"
            else:
                print "----------删除3天前备份失败----------"
        else:
            print "----------备份数据库失败----------"


b1 = Mysql(command, command_delete)
b1.backup()