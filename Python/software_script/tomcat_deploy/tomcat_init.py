#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/26'
#   motto:  'Good memory as bad written'


import subprocess
import time, sys
import platform
import psutil


class Tomcat(object):
    def __init__(self, Tomcat_Home, Tomcat_Log_Home, counnt=10):
        self.Tomcat_Home = Tomcat_Home
        self.Tomcat_Log_Home = Tomcat_Log_Home
        self.counnt = counnt

    def system_info(self):
        system_type = platform.system()
        system_version = platform.linux_distribution()
        system_bit = platform.architecture()
        Boot_Start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
        Host_Memory = psutil.virtual_memory().total / 1024
        Can_Use = psutil.virtual_memory().available / 1024
        ipaddress = str(psutil.net_if_addrs()['eth0'][0])
        processors = psutil.cpu_count(logical=False)

        print "||||||||||" + "\033[32m本机IP地址--->Eth0:" + "\033[31m %s\033[0m" % ipaddress.split(',')[1]
        print "||||||||||" + "\033[32m系统信息:\033[0m" + "\033[31m%s %s-%s %s\033[0m" % (
            system_type, system_version[0], system_version[1], system_bit[0])
        print "||||||||||" + "\033[32m本机启动时间:\033[0m" + "\033[31m%s\033[0m" % Boot_Start
        print "||||||||||" + "\033[32m本机总内存:\033[0m" + "\033[31m %sKB\033[0m" % Host_Memory + "\033[31m ---->%sMB \033[0m" % (
            Host_Memory / 1024)
        print "||||||||||" + "\033[32m本机可使用内存:\033[0m" + "\033[31m%sKB\033[0m" % Can_Use + "\033[31m ---->%sMB \033[0m" % (
            Can_Use / 1024)
        print "||||||||||" + "\033[32m本机cpu合数:\033[0m" + "\033[31m %s \033[0m" % processors

    def get_tomcat_pid(self):
        commandcheckoutpid = "ps aux | grep java | grep -v grep | grep 'jenkins_tomcat' | awk '{print $2}'"
        p = subprocess.Popen(commandcheckoutpid, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        # print "\033[32m Jenkins Is Starting \033[0m" + "\033[31mPID:%s\033[0m" % stdout
        return stdout

    def start_tomcat(self):
        if len(self.get_tomcat_pid().strip()) != 0:
            print "\033[32m Tomcat Is Started \033[0m"
        else:
            # Start Tomcat
            command_start_tomcat = "%s/bin/startup.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_start_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            print stdout

    def stop_tomcat(self):
        wait_sleep = 0
        if len(self.get_tomcat_pid().strip()) == 0:
            print "\033[32m Tomcat is Not Running \033[0m"
        else:
            command_stop_tomcat = "%s/bin/shutdown.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_stop_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            while (len(self.get_tomcat_pid().strip()) != 0):
                print "\nwaiting for processes to exit"
                wait_sleep += 1
                time.sleep(1)
                if wait_sleep == self.counnt:
                    command_Kill_tomcat = "kill -9 %s" % int(self.get_tomcat_pid().strip())
                    p = subprocess.Popen(command_Kill_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, shell=True)
                    stdout, stderr = p.communicate()
                    print "\033[32m Stop Tomcat is sucessful \033[0m"
                    break

    def useage(self):
        scrip_name = "jenkins.py"
        print "\033[32m script use \033[0m" + "./" + scrip_name + "\033[31m start|stop|restart|status\033[0m"
        print "or"
        print "\033[32m Script use \033[0m" + "python <path>/" + scrip_name + "\033[31m start|stop|restart|status\033[0m"

    def tomcat_log(self):
        command_tomcat_log = "tail -f %s/catalina.out " % self.Tomcat_Log_Home
        p = subprocess.Popen(command_tomcat_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        returncode = p.poll()
        try:
            while returncode is None:
                line = p.stdout.readline()
                returncode = p.poll()
                line = line.strip()
                print line
            print returncode
        except KeyboardInterrupt:
            print 'ctrl+d or z'


if __name__ == '__main__':
    Handle = Tomcat("/software/jenkins_tomcat", "/software/jenkins_tomcat/logs")
    if len(sys.argv) < 2:
        Handle.useage()
        sys.exit()
    elif sys.argv[1] == 'start':
        Handle.start_tomcat()
    elif sys.argv[1] == 'stop':
        Handle.stop_tomcat()
    elif sys.argv[1] == 'restart':
        Handle.stop_tomcat()
        time.sleep(5)
        Handle.start_tomcat()
    elif sys.argv[1] == 'info':
        Handle.system_info()
    elif sys.argv[1] == 'log':
        Handle.tomcat_log()
    elif sys.argv[1] == 'status':
        if len(Handle.get_tomcat_pid().strip()) != 0:
            print "\033[32m Tomcat Is Running is PID:\033[0m" + "\033[31m %s \033[0m" % Handle.get_tomcat_pid().strip()
        else:
            print "\033[32m Tomat Not Running \033[0m"
    else:
        Handle.useage()
