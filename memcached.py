#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/18'
#   motto:  'Good memory as bad written'

import psutil, sys, time
import subprocess


class Memcached(object):
    def __init__(self, processname):
        self.processname = processname

    def stop_memcacehd(self):
        print "\033[32mStop Memcached...............\033[0m"
        for process in psutil.process_iter():
            if process.name() == self.processname:
                process.kill()

    def start_memcached(self):
        print "\033[32mStart Memcached.............\033[0m"
        memcached_bin_home = '/software/memcached/bin/memcached'
        for port in range(11211, 11215):
            memcached_start_options = "%s -d -m 10 -u root -l 0.0.0.0 -p %s -c 512 -P /tmp/memcached.pid" % (
                memcached_bin_home, port)
            subprocess.call(memcached_start_options, shell=True)

    def get_memcacehd_info(self):
        for process in psutil.process_iter():
            if process.name() == self.processname:
                print "程序PID=>", process.pid, "\n", "启动路径=>", process.exe(), \
                    "\n", "运行用户=>", process.username(), "\n", "运行状态=>", process.status()


if __name__ == '__main__':
    memcacehd_process_name = 'memcached'
    run = Memcached(memcacehd_process_name)
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
