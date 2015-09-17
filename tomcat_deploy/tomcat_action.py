#!/usr/bin/python
# _*_coding:utf-8_*_
# __author__ = 'yulong'
# DATE:'15-9-16'

import subprocess
import urllib2
import time, sys


class Action_Tomcat(object):
    def status(self):
        req = urllib2.Request('http://10.90.10.200:8080/index.html')
        # 记录访问重试次数
        request_num = 0
        while True:
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

    def get_pid(self):
        pid = ''
        try:
            # 获取Tomcat_pid 方法
            get_pid = """ps aux | grep tomcat-python | grep -v "grep" | awk '{print $2}'"""
            ret_pid = subprocess.Popen(get_pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ret_pid.wait()
            for line in ret_pid.stdout.readlines():
                pid += line
        except UnboundLocalError, err:
            print "\033[31m########Didn't get to Tomcat-pid#######\033[0m"
        return int(pid)

    def start(self):
        tomcat_bin_home = "/software/tomcat-python/bin/"
        tomcat_start_script = "startup.sh"
        command = "%s%s" % (tomcat_bin_home, tomcat_start_script)
        start_tomcat = subprocess.Popen(command, shell=True)
        start_tomcat.wait()
        if start_tomcat.returncode == 0:
            print "\033[32m##########Tomcat Start successful##########\033[0m"
        else:
            print "\033[31m##########Tomcat Start Failed##########\033[0m"

    def stop(self):
        kill_pid_command = "kill -9 %s" % (self.get_pid())
        run_command = subprocess.Popen(kill_pid_command, shell=True)
        run_command.wait()
        if run_command.returncode == 0:
            print "\033[32m#######kill Tomcat process successsful#######\033[0m"
        else:
            print "\033[31m#######Kill TOmcat process Failed#######\033[0m"

    def restart(self):
        self.stop()
        print "Waitting..........5 seconds"
        for i in range(5):
            print "\033[32mNumber of seconds is %s\033[0m" % i
            time.sleep(1)
        self.start()
        print "\033[32m#########Waitting for monitoring URL..........#########\033[0m"
        time.sleep(5)
        self.status()


if __name__ == "__main__":
    action_list = ('start', 'stop', 'restart', 'status', '--help')
    help_info = """\033[32m
                ----Process help----
            %s: Start Tomcat service
            %s: Stop Tomcat service
            %s: Restart Tomcat service
            %s: Tomcat Service Status \033[0m
    """ % (action_list[0], action_list[1], action_list[2], action_list[3])
    run = Action_Tomcat()
    try:
        if sys.argv[1] == action_list[0]:
            run.start()
        elif sys.argv[1] == action_list[1]:
            run.stop()
        elif sys.argv[1] == action_list[2]:
            run.restart()
        elif sys.argv[1] == action_list[3]:
            run.status()
        elif sys.argv[1] == action_list[4]:
            print help_info
            print "--------------------The divider-------------------"
        else:
            print "Parameter error！！！！"
    except IndexError, err:
        print err
