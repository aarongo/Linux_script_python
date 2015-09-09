# _*_coding:utf-8_*_
__author__ = 'yulong'
import pexpect
import getpass
import paramiko
import interactive
import server_group


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

    def chose_user(self):
        user_group = []
        competence = []
        for key in server_group.server_user:
            user_group.append(key)
        for index, value in enumerate(user_group):
            print index, value
        chose_group = raw_input("选择你要操作的环境：")
        if chose_group.isdigit():
            chose_group = int(chose_group)
        for key in server_group.server_user.get(user_group[chose_group]):
            competence.append(key)
        for index, value in enumerate(competence):
            print index, value
        chose_competence = raw_input("选择你要以什么身份进行登录：")
        if chose_competence.isdigit():
            chose_competence = int(chose_competence)
            user = server_group.server_user.get(user_group[chose_group]).get(competence[chose_competence]).get("user")
            password = server_group.server_user.get(user_group[chose_group]).get(competence[chose_competence]).get(
                "password")
            info = user, password
        return info

    def put(self):
        pass

    def get(self):
        pass


if __name__ == "__main__":
    while True:
        print """
            \033[31m运行方式分为两种：
                ssh:----->直接登录到服务器进行操作
                command:----->执行单次命令获取到结果\033[0m
        """
        way = raw_input("\033[35m 请输入的方式：\033[0m").strip()
        if way == 'command':
            print "\033[32m---------------Command SHell Only---------------\033[0m"
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
            print "\033[32m---------------SSH To Server---------------\033[0m"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：").strip()
                pwd = getpass.getpass(prompt='输入密码: ')
                run.connection(ip, user, pwd)
            except IndexError, err:
                print "\033[31m你选择的环境/服务器组/主机不存在\033[0m"
        elif way == 'quit':
            print "----------\033[31m 退出 \033[0m----------"
            break
        else:
            print "--------------------\033[31m 输入的操作方式错误重新输入\033[0m--------------------"
