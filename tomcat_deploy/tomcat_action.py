#!/usr/bin/python
# _*_coding:utf-8_*_
# __author__ = 'yulong'
# DATE:'15-9-16'

import subprocess
import sys
import pexpect
import tomcat_conf
import os
import datetime


class Action_Tomcat(object):
    def send_password(self, command):
        command_output, exitstatus = pexpect.run(command, events={'(?i)password': 'comall2014\n'}, withexitstatus=1)
        print '=====>结果', command_output, '======>状态', exitstatus

    def svn_update(self, svn_number):
        # 执行远程SVN代码更新
        command_line1 = "%s update -r %s %s" % (tomcat_conf.svn_bin_home, svn_number, tomcat_conf.svn_checkout_dir)
        print "\033[32m***************Updating Project***************\033[0m"
        subprocess.call(command_line1, shell=True)
        print "\033[31m***************END**************\033[0m"

    def build_project(self):
        # 编译环境
        command_line2 = "cd %s && %s clean install  -Ptest -DskipTests" % (
            tomcat_conf.svn_checkout_dir, tomcat_conf.maven_bin_home)
        print "\033[32m***************Mavne Bulid Project***************\033[0m"
        subprocess.call(command_line2, shell=True)
        print "\033[31m***************END**************\033[0m"

    def war_handle(self):
        # First cp *.war to Unzip_tmp Dir
        if os.path.exists(tomcat_conf.unzip_tmp):
            for path in tomcat_conf.war_path:
                command_line3 = "cd %s && cp *.war %s" % (path, tomcat_conf.unzip_tmp)
                subprocess.call(command_line3, shell=True)
        else:
            print "\033[32m***************Mkdir Tmp Dir**************\033[0m"
            os.mkdir(tomcat_conf.unzip_tmp)
            for path in tomcat_conf.war_path:
                command_line3 = "cd %s && cp *.war %s" % (path, tomcat_conf.unzip_tmp)
                subprocess.call(command_line3, shell=True)
        ##################First End########################
        # Second unzip *.war
        if os.path.exists(tomcat_conf.unzip_war_front) and os.path.exists(tomcat_conf.unzip_war_web):
            print "\033[32m**************Dir Is exists***************\033[0m"
            print "\033[32m**************Unzip war***************\033[0m"
            command_line4 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_front, tomcat_conf.unzip_war_front)
            command_line5 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_web, tomcat_conf.unzip_war_web)
            subprocess.call(command_line4, shell=True)
            subprocess.call(command_line5, shell=True)
        else:
            for lists in os.listdir(tomcat_conf.unzip_tmp):
                path_tmp = os.path.join(tomcat_conf.unzip_tmp, lists).strip('.war')
                os.mkdir(path_tmp)
            command_line4 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_front, tomcat_conf.unzip_war_front)
            command_line5 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_web, tomcat_conf.unzip_war_web)
            command_line6 = "cd %s && rm -rf *.war" % tomcat_conf.unzip_tmp
            subprocess.call(command_line4, shell=True)
            subprocess.call(command_line5, shell=True)
            subprocess.call(command_line6, shell=True)

    def send_dir(self):
        print "\033[32m*****************scp War Dir***************\033[0m"
        print tomcat_conf.remote_host_dir
        for key in tomcat_conf.remote_host_dir.iteritems():
            command_line7 = "scp -r %s %s:%s" % (tomcat_conf.unzip_tmp, key[0], key[1])
            print command_line7
            self.send_password(command_line7)

if __name__ == "__main__":
    start = Action_Tomcat()
    # start.svn_update(sys.argv[1])
    # start.build_project()
    start.send_dir()
