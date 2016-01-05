#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"


import subprocess
import sys, argparse, os
import paramiko


class SSHConnection(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False

        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))

        self.transport.connect(username=username, password=password)

    # ----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True

    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)

    # ----------------------------------------------------------------------
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()


class SSHCommand(object):
    # 定义脚本执行时参数列表~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def check_arg(self, args=None):
        parser = argparse.ArgumentParser(description='Script to learn basic argparse')
        parser.add_argument('-H', '--host', help='host ip', required='True', choices=('172.31.1.101', '172.31.1.100'),
                            default='localhost')
        parser.add_argument('-u', '--user', help='user name', default='root')
        parser.add_argument('-t', '--type', help='Handle Type', default='status')

        if len(sys.argv) <= 2:
            parser.print_help()
            sys.exit(1)
        return parser.parse_args(args)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # 通过 subprocess 执行远程命令~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def run_cmd(self, arguments, command):
        try:
            host = arguments.host
            user = arguments.user
            ssh = ''.join(['ssh ', user, '@', host, ' '])
            cmd = ssh + command
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # proc.wait()
            (stdoutdata, stderrdata) = proc.communicate()
            if proc.returncode != 0:
                print "-" * 20 + "\033[31mError\033[0m" + "-" * 20
                print "\033[31mRemote Server Run Script %s Error\033[0m" % command + "\n" + stderrdata
                print "#" * 40
            else:
                print "-" * 20 + "\033[31mOUT\033[0m" + "-" * 20
                print stdoutdata
                print "-" * 40
        except KeyboardInterrupt:
            print "\033[31mQuit\033[0m" + "." * 20
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == '__main__':
    args = SSHCommand().check_arg(sys.argv[1:])
    # 执行过程中输入多个 ip 时中间有多个空格只保留一个
    # host = args.sub(r'\s+', ' ', args.host)
    if args.type == 'status':
        command = "/software/script/carrefour_app.py -c mobile -d %s" % args.type
        SSHCommand().run_cmd(args, command)
    elif args.type == 'start':
        command = "/software/script/carrefour_app.py -c mobile -d %s" % args.type
        SSHCommand().run_cmd(args, command)
    elif args.type == 'stop':
        command = "/software/script/carrefour_app.py -c mobile -d %s" % args.type
        SSHCommand().run_cmd(args, command)
    elif args.type == 'restart':
        command = "/software/script/carrefour_app.py -c mobile -d %s" % args.type
        SSHCommand().run_cmd(args, command)
    elif args.type == 'deploy':
        # 首先传送文件到部署服务器
        print "\033[31mSending Deploy Files To Remote Server" + "." * 40
        send = SSHConnection(args.host, args.user, password='comall2014')
        local_files = "/software/upload_war/cybershop-mobile-0.0.1-SNAPSHOT.war"
        remote_path = "/software/cybershop-mobile-0.0.1-SNAPSHOT.war"
        send.put(local_files, remote_path)
        send.close()
        print "\033[32mSend Files End!!!\033[0m"
        # 发送文件结束
        print "\033[31mWaiting Deploy\033[0m" + "." * 30
        command = "/software/script/carrefour_app.py -c mobile -d %s" % args.type
        SSHCommand().run_cmd(args, command)
    else:
        print "\033[31mPlease Input Right args ByeBye\033[0m" + "!" * 30
