#!/usr/bin/python
# _*_coding:utf-8_*_
# __author__ = 'yulong'
# DATE:'15-9-16'

import subprocess
import sys
import pexpect
import tomcat_conf


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


if __name__ == "__main__":
    start = Action_Tomcat()
    start.svn_update(sys.argv[1])
    start.build_project()
