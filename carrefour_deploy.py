#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
import paramiko
import argparse
import sys


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


class Run_Cmd(object):
    def Run(self, hostname, username, password, command, port=22, nbytes=4096):
        client = paramiko.Transport((hostname, port))
        client.connect(username=username, password=password)

        stdout_data = []
        stderr_data = []
        session = client.open_channel(kind='session')
        session.exec_command(command)
        while True:
            if session.recv_ready():
                stdout_data.append(session.recv(nbytes))
            if session.recv_stderr_ready():
                stderr_data.append(session.recv_stderr(nbytes))
            if session.exit_status_ready():
                break

        print 'exit status: ', session.recv_exit_status()
        print ''.join(stdout_data)
        print ''.join(stderr_data)

        session.close()
        client.close()


if __name__ == "__main__":
    username = "root"
    pw = "comall2014"
    parser = argparse.ArgumentParser(
            description="eg: '%(prog)s' -h ipaddress -d {front|web}")
    # ADD Tomcat Apps ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    parser.add_argument('-p', '--deploy_ipaddress', nargs='+', dest='choices',
                        choices=('10.90.0.244', '10.90.10.245'))  # choices 规定只能书写此处标出的, nargs='+' 至少有一个参数
    parser.add_argument('-d', '--Handle', action='store', nargs='?', dest='handle', choices=('front', 'web'),
                        help='Input One of the {front|web}')  # nargs='?' 有一个货没有参数都可以
    parser.add_argument('-t', '--action', action='store', nargs='+', dest='parameter',
                        choices=('log', 'start', 'stop', 'status', 'restart'),
                        help='operating Tomcat log|start|stop|status|restart')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    if len(sys.argv) <= 3:
        parser.print_help()
    else:
        try:
            send_files = SSHConnection(args.choices[0], username, pw)
            remote_script = Run_Cmd()
            if args.handle == 'front':
                # source_files = '/software/cybershop-front-0.0.1-SNAPSHOT.war'
                # dest_files = '/software/cybershop-front-0.0.1-SNAPSHOT.war'
                # send_files.put(source_files, dest_files)
                send_files.close()
                command = "/root/deploy_front.py -c front -d deploy"
                remote_script.Run(hostname=args.choices[0], username=username, password=pw, command=command)
            if args.handle == 'web':
                source_files = '/software/cybershop-web-0.0.1-SNAPSHOT.war'
                dest_files = '/software/cybershop-web-0.0.1-SNAPSHOT.war'
                send_files.put(source_files, dest_files)
                send_files.close()
                command = "/root/deploy_backend.py -c backend -d deploy"
                remote_script.Run(hostname=args.choices[0], username=username, password=pw, command=command)
        except TypeError:
            parser.print_help()
