#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/26'
#   motto:  'Good memory as bad written'


import psutil
from subprocess import PIPE
import time
import platform
import sys
import requests


class Tomcat(object):
    def __init__(self, Tomcat_Home):
        self.Tomcat_Home = Tomcat_Home

    def system_info(self):
        system_type = platform.system()
        system_version = platform.linux_distribution()
        system_bit = platform.architecture()
        print "\033[32m系统信息:\033[0m" + "\033[31m%s %s-%s %s\033[0m" % (
            system_type, system_version[0], system_version[1], system_bit[0])
        Boot_Start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
        print "\033[32m本机启动时间:\033[0m" + "\033[31m%s\033[0m" % Boot_Start
        Host_Memory = psutil.virtual_memory().total / 1024
        print "\033[32m本机总内存:\033[0m" + "\033[31m %sKB\033[0m" % Host_Memory + "\033[31m ---->%sMB \033[0m" % (
            Host_Memory / 1024)
        Can_Use = psutil.virtual_memory().available / 1024
        print "\033[32m本机可使用内存:\033[0m" + "\033[31m%sKB\033[0m" % Can_Use + "\033[31m ---->%sMB \033[0m" % (
            Can_Use / 1024)
        ipaddress = str(psutil.net_if_addrs()['eth0'][0])
        print "\033[32m本机IP地址--->Eth0:" + "\033[31m %s\033[0m" % ipaddress.split(',')[1]

    def start(self):
        # start jenkins
        Tomcat_bin = "%s/bin/startup.sh" % self.Tomcat_Home
        p = psutil.Popen(Tomcat_bin, stdout=PIPE)
        return p



    def stop(self):
        # Stop Tomcat
        self.start().kill()


if __name__ == '__main__':
    Tomcat_handle = Tomcat("/software/jenkins_tomcat")
    try:
        if sys.argv[1] == 'info':
            Tomcat_handle.system_info()
        elif sys.argv[1] == 'start':
            Tomcat_handle.start()
        elif sys.argv[1] == 'stop':
            Tomcat_handle.stop()
        elif sys.argv[1] == 'restart':
            Tomcat_handle.stop()
            time.sleep(5)
            Tomcat_handle.start()

        else:
            print "\033[31m Please input parameter\033[0m"
    except IndexError, err:
        print err
