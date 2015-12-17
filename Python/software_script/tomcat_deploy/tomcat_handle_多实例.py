#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author "Edward.Liu"

# Import libary~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import subprocess
import time
import sys
import signal
import os
import argparse


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Tomcat(object):
    def __init__(self, tomcat_exe):
        self.tomcat_exe = tomcat_exe
        self.Tomcat_Home = "/install/%s" % tomcat_exe
        self.Tomcat_Log_Home = "/install/%s/logs" % tomcat_exe
        self.counnt = 10
        self.Tomcat_Examples = ['tomcat', 'tomcat-mobile']

    # Get Tomcat_PID~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def get_tomcat_pid(self):
        # 自定义获取程序 pid 与启动命令
        p = subprocess.Popen(['ps', '-Ao', 'pid,command'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'java' in line:
                if self.tomcat_exe in line:
                    pid = int(line.split(None, 1)[0])
                    return pid
                    # 获取 END

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
    parser = argparse.ArgumentParser(
            description="eg: '%(prog)s' -c tomcat|tomcat-mobile -d {start|stop|status|restart|log}")
    # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parser.add_argument('-c', '--app_name', nargs='+', dest='choices',
                        choices=('tomcat', 'tomcat-mobile'))  # choices 规定只能书写此处标出的, nargs='+' 至少有一个参数
    parser.add_argument('-d', '--Handle', action='store', nargs='?', dest='handle', default='log',
                        help='Input One of the {start|stop|status|restart|log}')  # nargs='?' 有一个货没有参数都可以
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    if len(sys.argv) <= 4:
        parser.print_help()
    else:
        try:
            Handle = Tomcat(args.choices[0])
            if args.handle == 'log':
                Handle.tomcat_log()
            elif args.handle == 'start':
                Handle.start_tomcat()
            elif args.handle == 'stop':
                Handle.stop_tomcat()
            elif args.handle == 'restart':
                Handle.stop_tomcat()
                time.sleep(5)
                Handle.start_tomcat()
            elif args.handle == 'status':
                if Handle.get_tomcat_pid() is not None:
                    print "\033[32m %s Is Running is PID:\033[0m" % Handle.tomcat_exe + "\033[31m %s \033[0m" % Handle.get_tomcat_pid()
                else:
                    print "\033[32m %s Not Running Or Not Exist \033[0m" % Handle.tomcat_exe
            else:
                print "\033[31mYou Input parameter Is Not Exist\033[0m"
        except TypeError:
            parser.print_help()
