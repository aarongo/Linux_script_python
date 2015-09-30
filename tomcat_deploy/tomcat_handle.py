#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/9/28'
#   motto:  'Good memory as bad written'

import urllib2
import time
import subprocess
import handle_conf
import sys


class Tomcat(object):
    def status(self):
        # 记录访问重试次数
        request_num = 0
        while True:
            URL = "http://172.31.0.253/login"
            req = urllib2.Request(URL)
            try:
                response = urllib2.urlopen(req)
                if response.code == 200:
                    print "\033[32m The Tomcat Server is normal! Return Code：%s\033[0m" % response.code
                    break
            except urllib2.HTTPError, err:
                print "\033[31m URL Access exception---->Return Code：%s Tomcat Is not normal ---->Retry Access 5 number\033[0m" % err.code
                time.sleep(3)
                request_num += 1
                if request_num == 5:
                    print "\033[31m Retry%snumber Still cannot access, please contact your administrator\033[0m" % request_num
                    break
            except urllib2.URLError, e:
                print "\033[31m Tomcat Not Runnint or access URL is Not exist Access info = %s\033[0m" % e
                break

    # 后台程序的操作
    def get_pid_back(self):
        pid = ''
        try:
            # 获取Tomcat_pid 方法
            # get_pid = """ps aux | grep tomcat-front | grep -v "grep" | awk '{print $2}'"""
            get_pid = """ps aux | grep tomcat | grep "tomcat-back" | grep -v "grep" | awk '{print $2}'"""
            ret_pid = subprocess.Popen(get_pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ret_pid.wait()
            for line in ret_pid.stdout.readlines():
                pid += line
        except UnboundLocalError, err:
            print "\033[31m########Didn't get to Tomcat-pid#######\033[0m"
        return int(pid)

    def start_back(self):
        # 1,启动 Tomcat 容器
        tomcat_bin_home = "%s/bin/" % handle_conf.Tomcat_webapps_back
        tomcat_start_script = "startup.sh"
        command = "%s%s" % (tomcat_bin_home, tomcat_start_script)
        start_tomcat = subprocess.Popen(command, shell=True)
        start_tomcat.wait()
        if start_tomcat.returncode == 0:
            print "\033[32m ##########Tomcat-Back Start successful########## \033[0m"
        else:
            print "\033[31m ##########Tomcat-Back Start Failed##########\033[0m"

    def stop_back(self):
        # 1,停止 Tomcat 容器
        kill_pid_command = "kill -9 %s" % (self.get_pid_back())
        run_command = subprocess.Popen(kill_pid_command, shell=True)
        run_command.wait()
        if run_command.returncode == 0:
            print "\033[32m #######kill Tomcat process successsful#######\033[0m"
        else:
            print "\033[31m #######Kill TOmcat process Failed#######\033[0m"

    def link_on_back(self):
        print "\033[32m#############Link On Tomcat-back Project and Upload###############"
        # 连接图片目录(Web)
        link_project = "ln -s %s/%s %s" % (
            handle_conf.project_dir, handle_conf.project_back_name, handle_conf.Tomcat_Deploy_Dir_Back)
        link_command = "ln -s %s %s" % (handle_conf.Mount_Dir, handle_conf.Back_Link_Dir)
        subprocess.call(link_project, shell=True)
        subprocess.call(link_command, shell=True)

    def link_off_back(self):
        print "\033[32m################Link Off Tomcat-Back Project and Upload###############\033[0m"
        # ,首先删除软连接符号  3,清除 Tomcat 残留文件
        # 删除 upload软连接
        unlinks_upload = "rm -f %s" % handle_conf.Back_Link_Dir
        # 删除 tomcat work 文件夹下
        delete_tocmat_tmp_command = "rm -rf %s*" % handle_conf.Tomcat_BackTmp_Dir
        # 删除 project 软连接
        unlinks_project = "rm -f %s" % handle_conf.Tomcat_Deploy_Dir_Back
        print unlinks_upload
        print delete_tocmat_tmp_command
        print unlinks_project
        # 首先删除 upload 软连接
        subprocess.call(unlinks_upload, shell=True)
        # 删除 project 软连接
        subprocess.call(unlinks_project, shell=True)
        # 清除 tomcat work 目录
        subprocess.call(delete_tocmat_tmp_command, shell=True)

    # 后台操作完毕
    # 前台操作
    def link_on_front(self):
        print "\033[32m###############Link On Tomcat-Front Project and upload###############\033[0m"
        # 连接图片目录(Front)
        # 连接项目
        print "\033[32m###############Link On tomcat-front Project and upload##############\033[0m"
        project_link = "ln -s %s/%s %s" % (
            handle_conf.project_dir, handle_conf.project_front_name, handle_conf.Tomcat_Deploy_Dir_Front)
        # link_upload = "ln -s %s %s" % (handle_conf.Mount_Dir, handle_conf.Front_Link_Dir)
        print project_link
        # print link_upload
        subprocess.call(project_link, shell=True)
        # subprocess.call(link_upload, shell=True)

    def link_off_front(self):
        print "\033[32m###############Link off Tomcat-Front Project and upload################\033[m"
        # ,首先删除软连接符号  3,清除 Tomcat 残留文件
        print "\033[32m###############UnLink Tomcat-Front Project and Upload###############\033[0m"
        # 卸载 upload 目录
        # unlinks_command = "rm -f %s" % handle_conf.Front_Link_Dir
        # 卸载项目目录
        unlink_project = "rm -f %s" % handle_conf.Tomcat_Deploy_Dir_Front
        delete_tocmat_tmp_command = "rm -rf %s*" % handle_conf.Tomcat_FrontTmp_Dir
        # 删除项目
        remove_old_project = "rm -rf %s/%s" % (handle_conf.project_dir, handle_conf.project_front_name)
        subprocess.call(unlink_project, shell=True)
        subprocess.call(delete_tocmat_tmp_command, shell=True)

    def get_pid_front(self):
        pid = ''
        try:
            # 获取Tomcat_pid 方法
            # get_pid = """ps aux | grep tomcat-front | grep -v "grep" | awk '{print $2}'"""
            get_pid = """ps aux | grep tomcat | grep "tomcat-front" | grep -v "grep" | awk '{print $2}'"""
            ret_pid = subprocess.Popen(get_pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ret_pid.wait()
            for line in ret_pid.stdout.readlines():
                pid += line
        except UnboundLocalError, err:
            print "\033[31m########Didn't get to Tomcat-pid#######\033[0m"
        return int(pid)

    def start_front(self):
        # 1,启动 Tomcat 容器
        tomcat_bin_home = "%s/bin/" % handle_conf.Tomcat_webapps_front
        tomcat_start_script = "startup.sh"
        command = "%s%s" % (tomcat_bin_home, tomcat_start_script)
        start_tomcat = subprocess.Popen(command, shell=True)
        start_tomcat.wait()
        if start_tomcat.returncode == 0:
            print "\033[32m ##########Tomcat-Front Start successful########## \033[0m"
        else:
            print "\033[31m ##########Tomcat-Front Start Failed##########\033[0m"

    def stop_front(self):
        # 1,停止 Tomcat 前台容器
        print "\033[32m################Stop Tomcat-Front###############\033[0m"
        kill_pid_command = "kill -9 %s" % (self.get_pid_front())
        run_command = subprocess.Popen(kill_pid_command, shell=True)
        run_command.wait()
        if run_command.returncode == 0:
            print "\033[32m #######kill Tomcat process successsful#######\033[0m"
        else:
            print "\033[31m #######Kill TOmcat process Failed#######\033[0m"

    # 前台操作完毕
    def restart_front(self):
        self.stop_front()
        print "\033[32m*****Waitting..........5 seconds\033[0m"
        for i in range(5):
            print "\033[32mNumber of seconds is %s\033[0m" % i
            time.sleep(1)
        self.start_front()
        print "\033[32m#########Waitting for monitoring URL..........#########\033[0m"
        time.sleep(5)
        self.status()

    def restart_back(self):
        self.stop_back()
        print "\033[32m*****Waitting..........5 seconds\033[0m"
        for i in range(5):
            print "\033[32mNumber of seconds is %s\033[0m" % i
            time.sleep(1)
        self.start_back()
        print "\033[32m#########Waitting for monitoring URL..........#########\033[0m"
        time.sleep(5)
        self.status()


if __name__ == "__main__":
    action_list = ('start', 'stop', 'restart', 'status')
    help_info = """
                ----Process help----
            %s: Start Tomcat service
            %s: Stop Tomcat service
            %s: Restart Tomcat service
            %s: Tomcat Service Status
            eg: ./tomcat.py help
    """ % (action_list[0], action_list[1], action_list[2], action_list[3])
    frist = Tomcat()
    try:
        if sys.argv[1] == 'start_front':
            frist.start_front()
        elif sys.argv[1] == 'start_back':
            frist.start_back()
        elif sys.argv[1] == 'stop_front':
            frist.stop_front()
        elif sys.argv[1] == 'stop_back':
            frist.stop_back()
        elif sys.argv[1] == 'restart_front':
            frist.restart_front()
        elif sys.argv[1] == 'restart_back':
            frist.restart_back()
        elif sys.argv[1] == 'status':
            frist.status()
        elif sys.argv[1] == 'help':
            print help_info
        elif sys.argv[1] == 'link_on_front':
            frist.link_on_front()
        elif sys.argv[1] == 'link_on_back':
            frist.link_on_back()
        elif sys.argv[1] == 'link_off_front':
            frist.link_off_front()
        elif sys.argv[1] == 'link_off_back':
            frist.link_off_back()
    except IndexError, err:
        print "\033[31mPlease bring parameters execution!!!\033[0m"
