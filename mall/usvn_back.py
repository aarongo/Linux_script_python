#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/16'
#   motto:  'Good memory as bad written'
import time
import os, sys
import subprocess


class USVN(object):
    def __init__(self, remotely_ipaddress, usvn_files, back_directory, now=time.strftime('%Y-%m-%d-%H')):
        self.now = now
        self.remotely_ipaddress = remotely_ipaddress
        self.usvn_files = usvn_files
        self.back_directory = back_directory

    def cur_file_dir(self):
        # 获取脚本路径
        path = sys.path[0]
        # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def transmit(self):
        # Packaging
        back_fiels_name = "%s.tgz" % self.now
        tar_command = "tar czvf %s %s 2>&1 > /dev/null" % (back_fiels_name, self.usvn_files)
        subprocess.call(tar_command, shell=True)

        # transfils
        scp_command = "scp %s %s:%s && rm -rf %s/%s " % (
            back_fiels_name, self.remotely_ipaddress, self.back_directory, self.cur_file_dir(), back_fiels_name)
        subprocess.call(scp_command, shell=True)
        if os.path.exists(back_fiels_name):
            print "\033[31m backup usvn files Failed\033[0m"
        else:
            print "\033[32m backup usvn files Sucessful\033[0m"


if __name__ == "__main__":
    start_backup = USVN('172.31.1.160', '/software/usvn/files', '/install/backup/usvnback/')
    start_backup.transmit()
