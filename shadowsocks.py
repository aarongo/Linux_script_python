# _*_coding:utf-8_*_
__author__ = 'lonnyliu'
# For Ubuntu Shadowsocks(ubuntu 代理方式的脚本)

import subprocess


class Shadowsocks(object):
    def __init__(self, command):
        self.command = command
    def run(self):
        print "--------后台启动shadowsocks--------"
        com_start = subprocess.Popen(self.command,shell=True)
        com_start.wait()
        if com_start.returncode == 0:
            print "--------Running Shadowsocks suecessful--------"
        else:
            print "--------Running Shadowsocks Fail--------"
if __name__ == "__main__":
    command = "/software/python2.7.10/bin/sslocal -c /software/python2.7.10/shadowsocks.json -d start"
    shawdowsocks_run = Shadowsocks()
    shawdowsocks_run.run()