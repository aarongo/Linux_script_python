#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/12'
#   motto:  'Good memory as bad written'

import os
import subprocess
import time

import auto_config


class Install_Mysql(object):
    def software_mysql(self):
        global ret
        ret = -1
        # 安装软件
        print "\033[32m==========Install Software==========\033[0m"
        command_line1 = "yum -y install %s " % (auto_config.default_install_software)
        subprocess.call(command_line1, shell=True)
        if os.path.exists(auto_config.cmake_bin_path):
            print "\033[32m###########Cmake Is Installed##########\033[0m"
        else:
            print "\033[32m==========Compile and install Cmake==========\033[0m"
            command_line2 = "cd %s && wget %s && tar xzf %s.tar.gz && cd %s && ./configure && make && make install" % (
                auto_config.software_dir, auto_config.cmake33_d_url, auto_config.cmake_name, auto_config.cmake_name)
            subprocess.call(command_line2, shell=True)
        if os.path.exists(auto_config.mysql_bin):
            print "\033[32m##########Mysql Is Installed##########\033[0m"
            ret = 0
        else:
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

    def initialization_mysql(self):
        if ret == 0:
            print "\033[32m##########This Mysql Is Configed##########\033[0m"
        else:
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

    def reday_mysql(self):
        if os.path.exists(auto_config.software_dir):
            print "\033[32m##########Directory Exist ##########\033[0m"
            self.software_mysql()
            self.initialization_mysql()
        else:
            print "\033[31m##########Directory No Exist ##########\033[0m"
            os.makedirs(auto_config.software_dir)
            self.software_mysql()
            self.initialization_mysql()

    def software_memcached(self):
        # downdoads and install Rely  packages
        # Libevent
        if os.path.exists(auto_config.libevent_dir) and os.path.exists(auto_config.zlib_dir):
            print "\033[32m++++++++++Libevent zlib exists+++++++++++\033[0m"
        else:
            print "\033[32m#################DownLoad %s ##################" % auto_config.libevent_pack_name
            command_line1 = "yum -y install wget tar && cd %s && wget %s" % (
                auto_config.software_dir, auto_config.libevent_url)
            subprocess.call(command_line1, shell=True)
            command_line2 = "cd %s && tar xzf %s && cd %s && ./configure %s && make && make install" % (
                auto_config.software_dir, auto_config.libevent_pack_name, auto_config.libevent_name,
                auto_config.libevent_parameters)
            subprocess.call(command_line2, shell=True)
            # Zlib
            command_line3 = "cd %s && wget %s" % (auto_config.software_dir, auto_config.zlib_url)
            command_line4 = "cd %s && tar xzf %s && cd %s && ./configure %s && make && make install" % (
                auto_config.software_dir, auto_config.zlib_pack_name, auto_config.zlib_name,
                auto_config.zlib_paramenters)
            subprocess.call(command_line3, shell=True)
            subprocess.call(command_line4, shell=True)

    def install_memcached(self):
        # downloads and install memcacehd
        if os.path.exists(auto_config.memcached_install_dir):
            print "\033[32m++++++++++Memcacehd Is Installed++++++++++\033[0m"
        else:
            command_line1 = "cd %s && wget %s && tar xzf %s && cd %s && ./configure %s && make && make install" % (
                auto_config.software_dir, auto_config.memcached_url, auto_config.memcached_pack_name,
                auto_config.memcached_name, auto_config.memcached_parameters)
            subprocess.call(command_line1, shell=True)
            if os.path.exists(auto_config.memcached_install_dir):
                print "\033[32m++++++++++Install Memcached Success++++++++++\033[0m"
            else:
                print "\033[31m++++++++++Install Memcached Failed++++++++++\033[0m"

    def start_memcacehd(self):
        # start memacehd(11211-11214)
        command_line2 = "ps aux | grep memcached | grep -v grep | wc -l"
        p = subprocess.Popen(command_line2, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if int(out) != 0:
            print "\033[32m##########The Memcached Is Stared##########\033[0m"
        else:
            for i in auto_config.memcached_prot:
                command_line1 = "%s/bin/memcached -d -m 10 -u root -l 0.0.0.0 -p %s -c 512 -P /tmp/memcached.pid" % (
                    auto_config.memcached_install_dir, i)
                print "\033[32mStart Memcached port is %s....................\033[0m" % i
                subprocess.call(command_line1, shell=True)
                time.sleep(5)

    def software_mongodb(self):
        # 安装 mongodb
        if os.path.exists(auto_config.mongodb_default_dir):
            print "\033[32m##########Mongodb Is Installed##########\033[0m"
        else:
            if os.path.exists(auto_config.software_dir):
                command_line1 = "yum -y install wget tar && cd %s && wget %s && tar xzf %s && mv %s %s" % (
                    auto_config.software_dir, auto_config.mongodb_url, auto_config.mongodb_pack_name,
                    auto_config.mongodb_name,
                    auto_config.mongodb_default_dir)
                subprocess.call(command_line1, shell=True)
                print "\033[32m++++++++++Mongodb Install Suceessful++++++++++\033[0m"
                # 添加配置文件
                if os.path.exists(auto_config.mongodb_data_dir):
                    configfile_dir = "%s/mongodb.conf" % auto_config.mongodb_default_dir
                    files = open(configfile_dir, 'w')
                    for config in auto_config.mongodb_config:
                        files.write(config)
                    files.close()
                    print "\033[32m+++++++++++Mongodb.conf Added++++++++++\033[0m"
                else:
                    os.makedirs(auto_config.mongodb_data_dir)
                    configfile_dir = "%s/mongodb.conf" % auto_config.mongodb_default_dir
                    files = open(configfile_dir, 'w')
                    for config in auto_config.mongodb_config:
                        files.write(config)
                    files.close()
                    print "\033[32m+++++++++++Mongodb.conf Added++++++++++\033[0m"
            else:
                os.makedirs(auto_config.software_dir)
                command_line1 = "yum -y install wget tar && cd %s && wget %s && tar xzf %s && mv %s %s" % (
                    auto_config.software_dir, auto_config.mongodb_url, auto_config.mongodb_pack_name,
                    auto_config.mongodb_name,
                    auto_config.mongodb_default_dir)
                subprocess.call(command_line1, shell=True)
                print "\033[32m++++++++++Mongodb Install Suceessful++++++++++\033[0m"
                # 添加配置文件
                if os.path.exists(auto_config.mongodb_data_dir):
                    configfile_dir = "%s/mongodb.conf" % auto_config.mongodb_default_dir
                    files = open(configfile_dir, 'w')
                    for config in auto_config.mongodb_config:
                        files.write(config)
                    files.close()
                    print "\033[32m+++++++++++Mongodb.conf Added++++++++++\033[0m"
                else:
                    os.makedirs(auto_config.mongodb_data_dir)
                    configfile_dir = "%s/mongodb.conf" % auto_config.mongodb_default_dir
                    files = open(configfile_dir, 'w')
                    for config in auto_config.mongodb_config:
                        files.write(config)
                    files.close()
                    print "\033[32m+++++++++++Mongodb.conf Added++++++++++\033[0m"

    def start_mongodb(self):
        # 判断 mongodb 服务是否启动
        command_line1 = "ps aux | grep mongodb | grep -v 'grep'| wc -l"
        p = subprocess.Popen(command_line1, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if int(out) != 0:
            print "\033[32m##########Mongodb Server Is Started##########\033[0m"
        else:
            # 启动 mongodb
            command_line2 = "%s/mongod -f %s/mongodb.conf" % (
                auto_config.mongodb_bin_home, auto_config.mongodb_default_dir)
            subprocess.call(command_line2, shell=True)


if __name__ == "__main__":
    start = Install_Mysql()
    server_list = ['mysql', 'memcached', 'mongodb', 'quit']
    while True:
        try:
            for index, value in enumerate(server_list):
                print index, value
            chose_server = raw_input("\033[31mPlease Chose Input server:\033[0m")
            if chose_server.isdigit():
                chose_server = int(chose_server)
                if server_list[chose_server] == 'mysql':
                    start.reday_mysql()
                    break
                elif server_list[chose_server] == 'memcached':
                    start.software_memcached()
                    start.install_memcached()
                    start.start_memcacehd()
                    break
                elif server_list[chose_server] == 'mongodb':
                    start.software_mongodb()
                    start.start_mongodb()
                    break
                elif server_list[chose_server] == 'quit':
                    break
        except IndexError, err:
            print "\033[31mChose Error Please reselect\033[0m"
