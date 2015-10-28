#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/18'
#   motto:  'Good memory as bad written'

import sys, time
import subprocess
import os


class Inst_moudles(object):
    def public_code(self):
        TMP = '/tmp/packages'
        download_url = 'https://pypi.python.org/packages/source/p/psutil/psutil-3.2.2.tar.gz'
        command_download = 'wget -P %s %s' % (TMP, download_url)
        command_tar_pexpect = 'tar xzf %s/%s -C %s' % (TMP, os.path.split(download_url)[1], TMP)
        if '/usr/bin' in os.getenv('PATH').split(':'): python_bin = '/usr/bin/python'
        command_install = 'cd %s/%s && %s setup.py install' % (
            TMP, os.path.split(download_url)[1].split('.tar.gz')[0], python_bin)
        subprocess.call(command_download, shell=True)
        subprocess.call(command_tar_pexpect, shell=True)
        subprocess.call(command_install, shell=True)
        print command_install
        print command_tar_pexpect
        print command_download

    def install_moudles(self):
        TMP = '/tmp/packages'
        print "\033[32m----------Installing psutil----------\033[0m"
        print TMP
        if os.path.exists(TMP):
            self.public_code()
        else:
            os.makedirs(TMP)
            self.public_code()


class Memcached(object):
    def __init__(self, processname, memcached_bin_home, pid_path):
        self.processname = processname
        self.memcached_bin_home = memcached_bin_home
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
            print "\033[32m-----------Service does not exist||Starting Memcacehd----------\033[0m"

    def start_memcached(self):
        print "\033[32mStart Memcached.............\033[0m"
        for port in range(11211, 11215):
            memcached_start_options = "%s -d -m 10 -u root -l 0.0.0.0 -p %s -c 512 -P %s" % (
                self.memcached_bin_home, port, self.pid_path)
            subprocess.call(memcached_start_options, shell=True)
            print "\033[32m----------Start At Port %s ---------\033[0m" % port
            time.sleep(1)
        if os.path.exists(self.pid_path):
            print "\033[32mMemcached Start Successful\033[0m"

    def get_memcacehd_info(self):
        process_num = 0
        if os.path.exists(self.pid_path):
            for process in psutil.process_iter():
                if process.name() == self.processname:
                    print "程序PID=>", process.pid, "\n", "启动路径=>", process.exe(), \
                        "\n", "运行用户=>", process.username(), "\n", "运行状态=>", process.status()
                    process_num += 1
        if process_num == 0:
            print "\033[32mMemcached Is Don't Start\033[0m"
        else:
            print "\033[32m----------Memcached number of processes %s----------\033[0m" % process_num


if __name__ == '__main__':
    try:
        import psutil
    except ImportError, err:
        print "\033[32m-----------detected psutil Not installed||||Installing-----------\033[0m"
        Inst_moudles().install_moudles()
    memcached_process_name = 'memcached'
    memcached_pid_path = '/tmp/memcached.pid'
    memcached_bin_home = '/software/memcached/bin/memcached'
    run = Memcached(memcached_process_name, memcached_bin_home, memcached_pid_path)
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
