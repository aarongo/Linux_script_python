#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"


# Import Library~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
import time
import sys
import signal
import os


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Tomcat(object):
    def __init__(self):
        self.tomcat_exe = "tomcat-mobile"
        self.Tomcat_Home = "/install/tomcat-mobile"
        self.Tomcat_Log_Home = "/install/tomcat-mobile/logs"
        self.counnt = 10

    # Get Tomcat_PID~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_tomcat_pid(self):
        p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'java' in line:
                if self.tomcat_exe in line:
                    pid = int(line.split(None, 1)[0])
                    return pid

    # Start Tomcat Process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def start_tomcat(self):
        if self.get_tomcat_pid() is not None:
            print "\033[32m %s Is Started \033[0m" % self.tomcat_exe
        else:
            # Start Tomcat
            command_start_tomcat = "%s/bin/startup.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_start_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            print stdout, stderr

    # Stop Tomcat process~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def stop_tomcat(self):
        wait_sleep = 0
        if self.get_tomcat_pid() is None:
            print "\033[32m %s is Not Running\033[0m" % self.tomcat_exe + "~" * 20
        else:
            command_stop_tomcat = "%s/bin/shutdown.sh" % self.Tomcat_Home
            p = subprocess.Popen(command_stop_tomcat, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
            while (self.get_tomcat_pid() is not None):
                print "waiting for processes to exit\n"
                wait_sleep += 1
                time.sleep(1)
                if wait_sleep == self.counnt:
                    os.kill(self.get_tomcat_pid(), signal.SIGKILL)
                    print "\033[32m Stop Tomcat is sucessful \033[0m"
                    break

    # Usage Options ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def useage(self):
        scrip_name = "tomcat_api.py"
        print "\033[32m script use \033[0m" + "./" + scrip_name + "\033[31m start|stop|restart|status|log\033[0m"
        print "or"
        print "\033[32m Script use \033[0m" + "python <path>/" + scrip_name + "\033[31m start|stop|restart|status|log\033[0m"

    # View TomcatLogs~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    Handle = Tomcat()
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
    elif sys.argv[1] == 'log':
        Handle.tomcat_log()
    elif sys.argv[1] == 'status':
        if Handle.get_tomcat_pid() is not None:
            print "\033[32m %s Is Running is PID:\033[0m" % Handle.tomcat_exe + "\033[31m %s \033[0m" % Handle.get_tomcat_pid()
        else:
            print "\033[32m %s Not Running Or Not Exist \033[0m" % Handle.tomcat_exe
    else:
        Handle.useage()
        sys.exit()
