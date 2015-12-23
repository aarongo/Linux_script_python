# _*_coding:utf-8_*_
__author__ = 'lonnyliu'
import paramiko


def Run_Cmd(hostname, username, password, command, port=22, nbytes=4096):
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


nbytes = 4096
hostname = '10.90.0.200'
port = 22
username = 'root'
password = 'aarongo'
command = 'ping -c 4 www.baidu.com'
Run_Cmd(hostname, username, password, command, port, nbytes)
