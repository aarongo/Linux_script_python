# _*_coding:utf-8_*_
__author__ = 'yulong'
import pexpect
import getpass
import paramiko
import interactive
import server_group
import ConfigParser
import os, time


class Action(object):
    def choseIP(self):
        # 选择出来的环境列表
        tmp_milieu = []
        # 选择出来的服务组
        tmp_server = []
        # 选择出来的服务器组内主机
        tmp_server_ip = []
        # 获取要操作的IP
        ip = None
        # 获取字典中的环境可以添加到环境列表
        for key in server_group.server_ip:
            tmp_milieu.append(key)
        # 遍历选择出来的环境列表
        while True:
            for index, value in enumerate(tmp_milieu):
                print index, value
                # 选择环境下的服务器组
            chose_milieu = raw_input("\033[32m选择你要操作的环境:\033[0m")
            if chose_milieu.isdigit():
                chose_milieu = int(chose_milieu)
                # 将选择出来的服务器组添加到列表中
                for key in server_group.server_ip.get(tmp_milieu[chose_milieu]):
                    tmp_server.append(key)
                break
            else:
                print "\033[32m--------------------请输入以下所显示环境----------------------\033[0m"
        while True:
            # 遍历服务器组
            for index, value in enumerate(tmp_server):
                print index, value
            chose_server = raw_input("\033[32m选择你要操作的服务器组:\033[0m")
            if chose_server.isdigit():
                chose_server = int(chose_server)
                # 遍历服务器组，将组内主机添加到tmp_server_ip列表中
                for key in server_group.server_ip.get(tmp_milieu[chose_milieu]).get(tmp_server[chose_server]):
                    tmp_server_ip.append(key)
                break
            else:
                print "\033[32m--------------------请输入以下所显示服务器组----------------------\033[0m"
        while True:
            # 遍历tmp_server_ip列表，将ip获取出来
            for index, value in enumerate(tmp_server_ip):
                print index, value
            chose_ip = raw_input("\033[32m选择你要操作的IP:\033[0m")
            if chose_ip.isdigit():
                chose_ip = int(chose_ip)
                ip = tmp_server_ip[chose_ip]
                return ip
                break
            else:
                print "\033[32m--------------------请输入以下所显示IP----------------------\033[0m"

    def ssh_command(self, user, password, hostip, command):
        # 为 ssh 命令生成一个 spawn 类的子程序对象
        child = pexpect.spawn('ssh %s@%s "%s"' % (user, hostip, command))
        try:
            # 设置检测屏幕输出的字符，'password:'如果检测到就是0,后边依此类推1,2,3,以及等待命令返回结果时间（秒）
            index = child.expect(['password:', 'Are you sure you want to continue connecting (yes/no)?'], timeout=20)
            print index
            if index == 0:
                child.sendline(password)
            elif index == 1:
                child.sendline('yes\n')
                child.expect('password:')
                child.sendline(password)
            elif index == 3:
                print "\033[31m 链接超时！！\033[0m"
            # 发送命令到远程
            child.sendline(command)
            print "-------------------\033[32m 结果为 \033[0m------------------", child.read()
        except pexpect.EOF, err:
            print "EOF-------->", err
        except pexpect.TIMEOUT, err:
            print "TIMEOUT", err
        finally:
            print "##########################################################################"
            child.close()

    def connection(self, ip, user, password, port=22):
        # 记录日志
        paramiko.util.log_to_file('/tmp/test')

        # 建立ssh连接
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password, compress=True)

        # 建立交互式shell连接
        channel = ssh.invoke_shell()

        # 建立交互式管道
        interactive.interactive_shell(channel, user, ip)

        # 关闭连接
        channel.close()
        ssh.close()

    def get_files(self, user, password, ip, port=22):
        print """
                ****************************************
                            批量传送文件
                   会将远程主机目录下所有文件传送到
                   本机目录下

                   如：scp /datadb/* user@hostname:/root/test/
                ××××××××××××××××××××××××××××××××××××××××
              """
        default_remote_path = "/root/test/"
        default_local_path = "/datadb/"
        remote_path = raw_input("请输入远程目录(默认为:/root/test/):").strip()
        if len(remote_path) == 0:
            remote_path = default_remote_path
        local_path = raw_input("请输入本机目录（默认为:/datadb/ 下载到本机的目录)").strip()
        if len(local_path) == 0:
            local_path = default_local_path
        t = paramiko.Transport((ip, port))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        files = sftp.listdir(remote_path)
        try:
            for f in files:
                print ''
                print "############################################"
                print "开始从%s下载文件 %s" % (ip, time.strftime("%Y-%m-%d %H:%M:%S"))
                print "下载文件：", os.path.join(remote_path, f)
                sftp.get(os.path.join(remote_path, f), os.path.join(local_path, f))
                print "成功下载文件 %s" % time.strftime("%Y-%m-%d %H:%M:%S")
                print "############################################"
        except IOError, err:
            print "有目录存在", err
        t.close()

    def put_files(self, user, password, ip, port=22):
        print """
                ****************************************
                            批量传送文件
                   会将本机目录下的所有文件传送到
                   远程主机目录下
                   如：scp /datadb/* user@hostname:/root/test/
                ××××××××××××××××××××××××××××××××××××××××
              """
        default_remote_path = "/root/test/"
        default_local_path = "/datadb/"
        remote_path = raw_input("请输入远程目录(默认为:/root/test/):").strip()
        if len(remote_path) == 0:
            remote_path = default_remote_path
        local_path = raw_input("请输入本机目录（默认为:/datadb/ 下载到本机的目录)").strip()
        if len(local_path) == 0:
            local_path = default_local_path
        t = paramiko.Transport((ip, port))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        files = os.listdir(local_path)
        try:
            for f in files:
                print ''
                print '#########################################'
                print '开始上传文件 %s ' % time.strftime("%Y-%m-%d %H:%M:%S")
                print '正在上传文件:', os.path.join(local_path, f)

                sftp.put(os.path.join(local_path, f), os.path.join(remote_path, f))

                print '开始上传文件 %s ' % time.strftime("%Y-%m-%d %H:%M:%S")

                print '上传文件成功 %s ' % time.strftime("%Y-%m-%d %H:%M:%S")
                print ''
                print '##########################################'
        except IOError, err:
            print "有目录存在", err
        t.close()

    def send_group(self):
        pass


if __name__ == "__main__":
    while True:
        print """
            \033[31m运行方式分为4种：
                ssh:==========直接登录到服务器进行操作
            command:==========执行单次命令获取到结果
                get:==========下载文件到本机
                put:==========上传文件到远程\033[0m
        """
        way = raw_input("\033[35m 请输入的方式：\033[0m").strip()
        if way == 'command':
            print "\033[32m---------------执行一条命令方式---------------\033[0m"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：").strip()
                pwd = getpass.getpass(prompt='输入密码: ')
                command = raw_input("输入要执行的命令：").strip()
                run.ssh_command(user, pwd, ip, command)
            except IndexError, err:
                print "\033[31m你选择的环境/服务器组/主机不存在\033[0m"


        elif way == 'ssh':
            print "\033[32m---------------连接到服务器方式---------------\033[0m"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：").strip()
                pwd = getpass.getpass(prompt='输入密码: ')
                run.connection(ip, user, pwd)
            except IndexError, err:
                print "\033[31m你选择的环境/服务器组/主机不存在\033[0m"


        elif way == 'get':
            print "\033[32m---------------下载远程文件到本机---------------\033[0m"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：").strip()
                pwd = getpass.getpass(prompt='输入密码: ')
                run.get_files(user, pwd, ip)
            except IndexError, err:
                print "\033[31m你选择的环境/服务器组/主机不存在\033[0m"


        elif way == 'put':
            print "\033[32m---------------上传文件到远程---------------\033[0m"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：").strip()
                pwd = getpass.getpass(prompt='输入密码: ')
                run.put_files(user, pwd, ip)
            except IndexError, err:
                print "\033[31m你选择的环境/服务器组/主机不存在\033[0m"

        elif way == 'quit':
            print "----------\033[31m 退出 \033[0m----------"
            break
        else:
            print "--------------------\033[31m 输入的操作方式错误重新输入\033[0m--------------------"
