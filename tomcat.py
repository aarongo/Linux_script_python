# _*_coding:utf-8_*_
__author__ = 'Lonny.Liu'
'''
    Author       lonnyliu
    Use Of      Linux Tomcat
    Time        2015-08-25
    Email       lonnyliu@126.com
'''
import subprocess
import time, datetime
import os

action_start = ['start', 'stop', 'restart', 'info', 'detect']
home = "/install/tomcat/"
tomcat_log = "%slogs" % (home)
script = "startup.sh"
command_start = "%sbin/%s" % (home, script)
tomcat_pid = """ ps aux | grep tomcat | grep -v "grep" | awk '{print $2}' > /root/pid.txt"""
now = datetime.datetime.now().strftime("%Y-%m-%d-%H")


class MyTomcat(object):
    def __init__(self, home, script, command_start, ):
        self.home = home
        self.script = script
        self.command_start = command_start

    def start(self):
        print "Running start"
        com_start = subprocess.Popen(self.command_start, shell=True)
        com_start.wait()
        if com_start.returncode == 0:
            print "--------String Tomcat Sucessful--------"
        else:
            print "--------String Tomcat Fail--------"

    def stop(self):
        print "Running stop"
        get_pid = subprocess.Popen(tomcat_pid, shell=True)
        get_pid.wait()
        pid = file("/root/pid.txt", "r")
        pid_num = pid.readline().strip()
        stop = "kill -9 %s" % pid_num
        com_stop = subprocess.Popen(stop, shell=True)
        com_stop.wait()
        pid.close()
        if com_stop.returncode == 0:
            print "--------Stoping Tomcat Sucessful--------"
        else:
            print "--------Stoping Tomcat Fail--------"

    def info(self):
        print "Running info"
        print "--------Tomcat Running Info--------"
        pid = file("/root/pid.txt", "r")
        pid_num = pid.readline().strip()
        pid.close()
        for dir_path, subpaths, files in os.walk(tomcat_log):
            print '''
                    TOMCAT_PID:      %s
                    TOMCAT_HOME:     %s
                    DATE_TIME:       %s
                    TOMCAT_LOG_NUM : %s
            ''' % (pid_num, home, now, len(files))

    def restart(self):
        print "Running stop"
        get_pid = subprocess.Popen(tomcat_pid, shell=True)
        get_pid.wait()
        pid = file("/root/pid.txt", "r")
        pid_num = pid.readline().strip()
        stop = "kill -9 %s" % pid_num
        com_stop = subprocess.Popen(stop, shell=True)
        com_stop.wait()
        pid.close()
        if com_stop.returncode == 0:
            print "--------Stoping Tomcat Sucessful--------"
        else:
            print "--------Stoping Tomcat Fail--------"
        time.sleep(15)
        print "Running start"
        com_start = subprocess.Popen(self.command_start, shell=True)
        com_start.wait()
        if com_start.returncode == 0:
            print "--------String Tomcat Sucessful--------"
        else:
            print "--------String Tomcat Fail--------"


if __name__ == "__main__":
    while True:
        run = MyTomcat(home, script, command_start)
        print "\033[32m ------You need to enter one of the following!------\033[0m"
        for index, options in enumerate(action_start):
            print index, "---->", options
        action = raw_input("Please Input Your action:")
        # 判断用户输入操作，在类中是否存在方法
        if hasattr(run, action):
            operating = getattr(run, action)
            operating()
            break
        else:
            print "Your Input action is Not exist!"
