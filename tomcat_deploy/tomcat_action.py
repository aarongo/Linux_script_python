#!/usr/bin/env python
# _*_coding:utf-8_*_
# __author__ = 'yulong'
# DATE:'15-9-16'

import subprocess
import pexpect
import tomcat_conf
import os, sys


class Action_Tomcat(object):
    def send_password(self, command):
        command_output, exitstatus = pexpect.run(command, events={'(?i)password': '11qq```\n'}, withexitstatus=1)
        print command_output
        return exitstatus

    def svn_update(self, svn_number):
        # 执行远程SVN代码更新
        # 此处应该获取命令结果状态 提供 main 进行判断
        command_line1 = "%s update -r %s %s" % (tomcat_conf.svn_bin_home, svn_number, tomcat_conf.svn_checkout_dir)
        print "\033[32m***************Updating Project***************\033[0m"
        subprocess.call(command_line1, shell=True)
        print "\033[31m***************END**************\033[0m"

    def build_project(self):
        # 编译环境
        # 此处应该获取命令结果状态 提供 main 进行判断
        command_line2 = "cd %s && %s clean install  -Ptest -DskipTests" % (
            tomcat_conf.svn_checkout_dir, tomcat_conf.maven_bin_home)
        print "\033[32m***************Mavne Bulid Project***************\033[0m"
        subprocess.call(command_line2, shell=True)
        print "\033[31m***************END**************\033[0m"

    def war_handle(self):
        # First cp *.war to Unzip_tmp Dir
        if os.path.exists(tomcat_conf.project_dir):
            for path in tomcat_conf.war_path:
                command_line3 = "cd %s && cp *.war %s" % (path, tomcat_conf.project_dir)
                subprocess.call(command_line3, shell=True)
        else:
            print "\033[32m***************Mkdir Tmp Dir**************\033[0m"
            os.mkdir(tomcat_conf.project_dir)
            for path in tomcat_conf.war_path:
                command_line3 = "cd %s && cp *.war %s" % (path, tomcat_conf.project_dir)
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
            for lists in os.listdir(tomcat_conf.project_dir):
                path_tmp = os.path.join(tomcat_conf.project_dir, lists).strip('.war')
                os.mkdir(path_tmp)
            command_line4 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_front, tomcat_conf.unzip_war_front)
            command_line5 = "unzip %s.war -d %s" % (tomcat_conf.unzip_war_web, tomcat_conf.unzip_war_web)
            command_line6 = "cd %s && rm -rf *.war" % tomcat_conf.project_dir
            subprocess.call(command_line4, shell=True)
            subprocess.call(command_line5, shell=True)
            subprocess.call(command_line6, shell=True)

    def send_dir(self):
        print "\033[32m*****************scp War Dir***************\033[0m"
        print tomcat_conf.remote_host_dir
        for lists in os.listdir(tomcat_conf.project_dir):
            dir_name = os.path.join(tomcat_conf.project_dir, lists)
            for key in tomcat_conf.remote_host_dir.iteritems():
                command_line7 = "scp -r %s %s:%s" % (dir_name, key[0], key[1])
                if self.send_password(command_line7) == 0:
                    print "\033[32m**************Scp Files Sucessful***************\033[0m"
                else:
                    print "\033[31m**************Scp Files Failed*************\033[0m"


if __name__ == "__main__":
    start = Action_Tomcat()
    try:
        if sys.argv[1] == 'front':
            start.svn_update(sys.argv[2])
            start.build_project()
            start.war_handle()
            # 执行脚本
            command_line1 = "ssh %s@%s '/root/tomcat_handle.py stop_front'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line1)
            # 删除软件接
            command_line2 = "ssh %s@%s '/root/tomcat_handle.py link_off_front'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line2)
            start.send_dir()
            command_line3 = "ssh %s@%s '/root/tomcat_handle.py link_on_front'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line3)
            command_line4 = "ssh %s@%s '/root/tomcat_handle.py start_front'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line4)
        elif sys.argv[1] == 'web':
            start.svn_update(sys.argv[2])
            start.build_project()
            start.war_handle()
            # 执行脚本
            command_line1 = "ssh %s@%s '/root/tomcat_handle.py stop_back'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line1)
            # 删除软件接
            command_line2 = "ssh %s@%s '/root/tomcat_handle.py link_off_back'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line2)
            start.send_dir()
            command_line3 = "ssh %s@%s '/root/tomcat_handle.py link_on_back'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line3)
            command_line4 = "ssh %s@%s '/root/tomcat_handle.py start_back'" % (
                tomcat_conf.remote_host_user, tomcat_conf.remote_host_dir.keys()[0])
            start.send_password(command_line4)
    except IndexError, err:
        print "\033[31m################Must Input Two Parameters#################\033[0m"
