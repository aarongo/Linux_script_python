# _*_coding:utf-8_*_
'''Author       lonnyliu
    Use Of      Linux backup file
    Time        2015-08-21
    Email       lonnyliu@126.com
    Information mongodb backup
'''
import datetime
import subprocess
import os
import sys
# mongodb服务器信息
mongodb_ip = "10.90.6.28"
mongodb_port = 27017
mongodb_name = "axontrade_b2b2c_dev"
# 备份目录
back_dir = "/software/back/"
# 临时备份目录
back_dir_tmp = "%smongodb_tmp/" % (back_dir)
# 时间戳
now = datetime.datetime.now().strftime("%Y-%m-%d-%H")
# 创建临时备份目录
command_mk = "mkdir -p %smongodb_tmp" % (back_dir)
# 备份命令
command_dump = "/software/mongoDB/bin/mongodump -h %s:%s -d %s -o %s  > /dev/null" % (
    mongodb_ip, mongodb_port, mongodb_name, back_dir_tmp)
# 打包备份文件
command_tar = "cd %s && tar czPf %s-%s.tar.gz %s" % (back_dir_tmp, now, mongodb_name, mongodb_name)
# 统计文件大小
tar_dir = "%s%s-%s.tar.gz" % (back_dir_tmp, now, mongodb_name)
# 传送tar包到最终备份目录
command_mv = "cd %s && mv %s-%s.tar.gz %s" % (back_dir_tmp, now, mongodb_name, back_dir)
# 删除临时备份目录
command_rm = "rm -rf %s" % (back_dir_tmp)
# 删除几天前的备份
day = 1
command_delete = "find %s -mtime +%s -delete" % (back_dir, day)


class Mongodb(object):
    def __init__(self, command_mk, command_dump, command_tar, command_mv, command_rm, command_delete):
        self.command_mk = command_mk
        self.command_dump = command_dump
        self.command_tar = command_tar
        self.command_mv = command_mv
        self.command_rm = command_rm

    def backup(self):
        # 创建临时目录
        com_mk = subprocess.Popen(command_mk, shell=True)
        com_mk.wait()
        if com_mk.returncode == 0:
            print "--------\033[32m执行mongodb备份到临时文件目录 \033[0m--------"
            com_dump = subprocess.Popen(command_dump, shell=True)
            com_dump.wait()
            if com_dump.returncode == 0:
                print "--------\033[32m执行临时文件的打包\033[0m--------"
                com_tar = subprocess.Popen(command_tar, shell=True)
                com_tar.wait()
                tar_file_size = os.path.getsize(tar_dir) / 1024 / 1024
                print "Mongodb的备份文件大小为：%sM" % (tar_file_size)
                if com_tar.returncode == 0:
                    print "--------\033[32m执行最终备份 \033[0m-------"
                    com_mv = subprocess.Popen(command_mv, shell=True)
                    com_mv.wait()
                    if com_mv.returncode == 0:
                        print "--------\033[32m mongodb备份完成 \033[0m--------"
                        com_rm = subprocess.Popen(command_rm, shell=True)
                        com_rm.wait()
                        if com_rm.returncode == 0:
                            print "----------\033[32m 删除临时备份目录成功\033[0m----------"
                        else:
                            print "----------\033[31m 删除临时备份目录失败\033[0m----------"
                    else:
                        print "-------\033[31m mongodb备份失败 \033[0m--------"
                else:
                    print "-------\033[31m  执行最终备份失败 \033[0m-------"
            else:
                print "--------\033[31m 打包临时文件失败 \033[0m --------"
        else:
            print "--------\033[31m 执行mongodb备份到临时文件目录失败 \033[0m-------"

    def drop(self):
        #先获取文件个数
        for dir_path, subpaths, files in os.walk(back_dir):
            if len(files) > day:
                print "----------------\033[32m删除%s天前备份\033[0m--------" % day
                com_delete = subprocess.Popen(command_delete, shell=True)
                if com_delete.returncode == 0:
                    print "------- \033[32m 删除成功\033[0m-------"
                else:
                    print "--------\033[31m 删除失败\033[0m --------"


run = Mongodb(command_mk, command_dump, command_tar, command_mv, command_rm, command_delete)
run.backup()
run.drop()
