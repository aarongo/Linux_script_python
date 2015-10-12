#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/12'
#   motto:  'Good memory as bad written'

import auto_config
import os
import subprocess
import time


class Install_Mysql(object):
    def software(self):
        # 安装软件
        print "\033[32m==========Install Software==========\033[0m"
        command_line1 = "yum -y install %s " % (auto_config.default_install_software)
        subprocess.call(command_line1, shell=True)
        print "\033[32m==========Compile and install Cmake==========\033[0m"
        command_line2 = "cd %s && wget %s && tar xzf %s.tar.gz && cd %s && ./configure && make && make install" % (
            auto_config.software_dir, auto_config.cmake33_d_url, auto_config.cmake_name, auto_config.cmake_name)
        subprocess.call(command_line2, shell=True)
        print "\033[32m===========Install Mysql==========\033[0m"
        for index, version in enumerate(auto_config.version):
            print index, version
        chose_mysql_version = raw_input("\033[32mChost Mysql Version:\033[0m")
        if chose_mysql_version.isdigit():
            chose_mysql_version = int(chose_mysql_version)
            # 定义全局属性,方便后续复制文件使用
            global new_mysql_dir
            new_mysql_dir = auto_config.version[chose_mysql_version]
            if auto_config.version[chose_mysql_version] == auto_config.mysql51:
                command_line3 = "cd %s && wget %s && tar xzf %s.tar.gz && cd %s && %s" % (
                    auto_config.software_dir, auto_config.mysql51_d_url, auto_config.version[chose_mysql_version],
                    auto_config.version[chose_mysql_version], auto_config.compile_command)
                subprocess.call(command_line3, shell=True)
            elif auto_config.version[chose_mysql_version] == auto_config.mysql55:
                command_line4 = "cd %s && wget %s && tar xzf %s.tar.gz && cd %s && %s" % (
                    auto_config.software_dir, auto_config.mysql55_d_url, auto_config.version[chose_mysql_version],
                    auto_config.version[chose_mysql_version], auto_config.compile_command)
                subprocess.call(command_line4, shell=True)
            elif auto_config.version[chose_mysql_version] == auto_config.mysql56:
                command_line5 = "cd %s && wget %s && tar xzf %s.tar.gz && cd %s && %s" % (
                    auto_config.software_dir, auto_config.mysql56_d_url, auto_config.version[chose_mysql_version],
                    auto_config.version[chose_mysql_version], auto_config.compile_command)
                subprocess.call(command_line5, shell=True)

    def initialization(self):
        # 初始化数据库
        # create mysql user
        command_line1 = "useradd -s /sbin/nologin mysql && chown -R %s" % (auto_config.mysql_data)
        subprocess.call(command_line1, shell=True)
        print command_line1
        command_line2 = "cd %s/scripts && ./mysql_install_db --user=mysql --basedir=%s --datadir=%s" % (
            auto_config.mysql_bin, auto_config.mysql_bin, auto_config.mysql_data)
        subprocess.call(command_line2, shell=True)
        print command_line2
        # 复制配置文件
        command_line3 = "cp -f %s/%s/support-files/my-medium.cnf /etc/my.cnf" % (
            auto_config.software_dir, new_mysql_dir)
        subprocess.call(command_line3, shell=True)
        # 添加到系统命令
        command_line4 = "cd %s && cp support-files/mysql.server /etc/init.d/mysqld" % auto_config.mysql_bin
        subprocess.call(command_line4, shell=True)
        # 如果不启动 更改不了密码
        command_line5 = "/etc/init.d/mysqld start"
        subprocess.call(command_line5, shell=True)
        # 更改默认 root 密码
        pwd = raw_input("\033[32mPlease Input Root Password:\033[0m")
        all_host = "%"
        select_root_password = "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%s' IDENTIFIED BY '%s' WITH GRANT OPTION;" % (
            all_host, pwd)
        print select_root_password
        select_root_password_local = "GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '%s' WITH GRANT OPTION;" % pwd
        print select_root_password_local
        command_line6 = """%s/bin/mysql -uroot  -e "%s" """ % (auto_config.mysql_bin, select_root_password)
        command_line7 = """%s/bin/mysql -uroot  -e "%s" """ % (
            auto_config.software_dir, select_root_password_local)
        subprocess.call(command_line6, shell=True)
        subprocess.call(command_line7, shell=True)

    def first_reday(self):
        if os.path.exists(auto_config.software_dir):
            print "\033[32m##########Directory Exist ##########\033[0m"
            self.software()
            self.initialization()
        else:
            print "\033[31m##########Directory No Exist ##########\033[0m"
            os.makedirs(auto_config.software_dir)
            self.software()
            self.initialization()


if __name__ == "__main__":
    start = Install_Mysql()
    help_man = """
            此脚本为安装 mysql 实现自动化安装,所有的配置信息存放在 auto_config配置文件中
            脚本执行过程需要2步认为干预,
            1,选择 mysql 的版本
            2,进行 Mysql 的初始密码设定
                """
    print help_man
    time.sleep(20)
    start.first_reday()
