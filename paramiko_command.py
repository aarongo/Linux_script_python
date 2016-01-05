#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author: "Edward.Liu"
# Author-Email: lonnyliu@126.com


import paramiko

host = '172.31.1.160'
port = 22
username = 'root'
password = 'comall2014'
trans = paramiko.Transport((host, port))
trans.connect(username=username, password=password)

session = trans.open_channel("session")
# Once the channel is established, we can execute only one command.Â  To execute another command, we need to create another channel
# session.exec_command('/software/script/carrefour_mobile.py -c mobile -d deploy')
session.exec_command('df -HT')

exit_status = session.recv_exit_status()

stdout_data = []
stderr_data = []

while session.recv_ready():
    stdout_data.append(session.recv(nbytes=4096))
stdout_data = "".join(stdout_data)

while session.recv_stderr_ready():
    stderr_data.append(session.recv_stderr(nbytes=4096))
stderr_data = "".join(stderr_data)

print "exit status", exit_status
print "\033[31m===============output===============\033[0m"
print stdout_data
print "\033[31m===============Error===============\033[0m"
print stderr_data

# sftp = paramiko.SFTPClient.from_transport(trans)
# sftp.get('remote_path', 'local_path')
# sftp.put('local_path', 'remote_path')
# sftp.close()