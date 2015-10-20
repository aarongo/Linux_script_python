#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/18'
#   motto:  'Good memory as bad written'

import psutil, sys, time
import subprocess
import os


class Memcached(object):
    def __init__(self, processname, pid_path):
        self.processname = processname
        self.pid_path = pid_path

    def stop_memcacehd(self):
        if os.path.exists(self.pid_path):
            print "\033[32mStop Memcached...............\033[0m"
            for process in psutil.process_iter():
                if process.name() == self.processname:
                    process.kill()
                    print "\033[32m----------Stop %s ProcessID=%s user=%s Successful----------\033[0m" % (
                        process.name(), process.pid, process.username())
            os.remove(self.pid_path)
        else:
            print "\033[32m-----------Service does not exist||Starting Memcacehd----------"

    def start_memcached(self):
        print "\033[32mStart Memcached.............\033[0m"
        memcached_bin_home = '/software/memcached/bin/memcached'
        for port in range(11211, 11215):
            memcached_start_options = "%s -d -m 10 -u root -l 0.0.0.0 -p %s -c 512 -P %s" % (
                memcached_bin_home, port, self.pid_path)
            subprocess.call(memcached_start_options, shell=True)
            print "\033[32m----------Start At Port %s ---------\033[0m" % port
            time.sleep(1)
        if os.path.exists(self.pid_path):
            print "\033[32mMemcached Start Successful\033[0m"

    def get_memcacehd_info(self):
        if os.path.exists(self.pid_path):
            for process in psutil.process_iter():
                if process.name() == self.processname:
                    print "程序PID=>", process.pid, "\n", "启动路径=>", process.exe(), \
                        "\n", "运行用户=>", process.username(), "\n", "运行状态=>", process.status()
        else:
            print "\033[32mMemcached Is Don't Start\033[0m"


if __name__ == '__main__':
    memcached_process_name = 'memcached'
    memcached_pid_path = '/tmp/memcached.pid'
    run = Memcached(memcached_process_name, memcached_pid_path)
    try:
        if sys.argv[1] == 'info':
            run.get_memcacehd_info()
        elif sys.argv[1] == 'start':
            run.start_memcached()
        elif sys.argv[1] == 'stop':
            run.stop_memcacehd()
        elif sys.argv[1] == 'restart':
            run.stop_memcacehd()
            time.sleep(5)
            run.start_memcached()
    except IndexError, err:
        print "\033[32mPlease parameters(info|start|stop|restart)\033[0m"
