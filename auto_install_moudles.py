#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/20'
#   motto:  'Good memory as bad written'

import platform
import subprocess
import os


class System:
    # 获取系统类型
    def GetType(self):
        Type = platform.dist()[0]
        return Type

    # 获取系统版本
    def GetRelease(self):
        Release = platform.dist()[1]
        return Release

    def Installer(self):
        tmp = '/tmp/packages'
        download_url = 'https://pypi.python.org/packages/source/p/pexpect/pexpect-3.3.tar.gz'
        if self.GetType() == 'centos':
            if os.path.exists(tmp):
                command_download = 'wget -P %s %s' % (tmp, download_url)
                command_tar_pexpect = 'tar xzf %s/%s -C %s' % (tmp, os.path.split(download_url)[1], tmp)
                if '/usr/bin' in os.getenv('PATH').split(':'): python_bin = '/usr/bin/python'
                command_install = 'cd %s/%s && %s setup.py install' % (
                tmp, os.path.split(download_url)[1].split('.tar.gz')[0], python_bin)
                subprocess.call(command_download, shell=True)
                subprocess.call(command_tar_pexpect, shell=True)
                subprocess.call(command_install, shell=True)


if __name__ == '__main__':
    try:
        import pexpect
    except ImportError, err:
        System().Installer()
