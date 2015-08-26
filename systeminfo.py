# _*_coding:utf-8_*_
__author__ = 'Lonny.Liu'
import paramiko


class SystemInfo(object):
    def __init__(self, address, port, user, password, command):
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.command = command

    def tcp(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.address, self.port, self.user, self.password)
        stdin, stdout, stderr = ssh.exec_command(self.command)
        show_list = stdout.readlines()
        for i in range(len(show_list)):
            print show_list[i],
        ssh.close()


if __name__ in "__main__":
    # address = raw_input("Please Input Your ipaddress:")
    address = "172.31.1.160"
    # prot = int(raw_input("Please Input connection Port:"))
    prot = 22
    user = raw_input("Please Input Connection User:")
    password = raw_input("Please Input Connection Password:")
    command = raw_input("Please Input Your command:")
    #command = """ps aux|grep httpd|wc -l"""
    run = SystemInfo(address, prot, user, password, command)
    run.tcp()
