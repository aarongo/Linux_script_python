#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/5'
#   motto:  'Good memory as bad written'

import os
import subprocess
import time


class Auto_agent(object):
    def __init__(self, serverip, install_dir, zabbix_name="zabbix-2.4.6.tar.gz"):
        self.serverip = serverip
        self.install_dir = install_dir
        self.zabbix_name = zabbix_name

    def handle_file(self):
        ret = -1
        zabbix_files_dir = "%s/%s" % (os.path.split(os.path.realpath(__file__))[0], self.zabbix_name)
        if os.path.exists(zabbix_files_dir):
            ret = 0
        return ret

    def auto_install(self):
        # Install zabbix_agent
        zabbix_files_dir = "%s/%s" % (os.path.split(os.path.realpath(__file__))[0], self.zabbix_name)
        install_command = "tar xzf %s -C %s && cd %s && ./configure --prefix=%s --enable-agent && make install" % (
            zabbix_files_dir, os.path.split(os.path.realpath(__file__))[0], zabbix_files_dir.split('.tar.gz')[0],
            self.install_dir)
        print install_command
        time.sleep(5)
        subprocess.call(install_command, shell=True)

    def change_config(self):
        print "\033[32m Change zabbix_agent file serverIP\033[0m"
        config_path = "%s/etc/zabbix_agentd.conf" % self.install_dir
        command_sed = "sed -i 's/127.0.0.1/%s/g' %s" % (self.serverip, config_path)
        print command_sed
        subprocess.call(command_sed, shell=True)

    def start_agent(self):
        print "\033[32m Start zabbix_agent AND Create user zabbix \033[0m"
        command_start = "useradd -s /sbin/nologin -g zabbix zabbix && %s/sbin/zabbix_agentd" % self.install_dir
        subprocess.call(command_start, shell=True)


if __name__ == "__main__":
    default_dir = '/software/zabbix_agent'
    default_ip = '127.0.0.1'
    Server_ip = raw_input("\033[32mPlease Input Server IP address(Default is 127.0.0.1)\033[0m").strip()
    Tmp_dir = raw_input("\033[32mPlease Input agent install Dirtory(Default is /software/zabbix_agent)\033[0m").strip()
    print len(Tmp_dir)
    if len(Tmp_dir) == 0 and len(Server_ip) != 0:
        start = Auto_agent(Server_ip, default_dir)
    elif len(Server_ip) == 0 and len(Tmp_dir) != 0:
        start = Auto_agent(default_ip, Tmp_dir)
    else:
        start = Auto_agent(default_ip, default_dir)

    if os.path.exists("/software"):
        if start.handle_file() == 0:
            start.auto_install()
            start.change_config()
            start.start_agent()
        else:
            print "\033[31mZabbix install Files Not exists Please Send Files\033[0m"
    else:
        os.makedirs("/software")
        if start.handle_file() == 0:
            start.auto_install()
            start.change_config()
            start.start_agent()
        else:
            print "\033[31mZabbix install Files Not exists Please Send Files\033[0m"
