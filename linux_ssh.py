# _*_coding:utf-8_*_
__author__ = 'yulong'
import pexpect
import getpass
import paramiko
import interactive
import server_group

server_ip = {
    "carrefour_test": {
        "backen_ip": ['172.31.1.100', '172.31.1.200'],
        "Front_ip": ['172.31.1.101', '172.31.1.201'],
        "Release_ip": ['172.31.1.160'],
        "Solr_ip": ['172.31.1.155'],
        "Memcached_ip": ['172.31.1.105', '172.31.1.102']
    },
    "B2B2C_Test": {
        "Backen_IP": ['10.90.6.27', '10.90.6.31'],
        "Front_IP": ['10.90.6.25', '10.90.6.26'],
        "Solr_IP": ['10.90.6.28', '10.90.6.29', '10.90.6.30'],
        "Images_ip": ['10.90.6.32']
    }
}


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
        for index, value in enumerate(tmp_milieu):
            print index, value
        chose_milieu = raw_input("选择你要操作的环境:")
        # 选择环境下的服务器组
        if chose_milieu.isdigit():
            chose_milieu = int(chose_milieu)
            # 将选择出来的服务器组添加到列表中
            for key in server_group.server_ip.get(tmp_milieu[chose_milieu]):
                tmp_server.append(key)
        # 遍历服务器组
        for index, value in enumerate(tmp_server):
            print index, value
        chose_server = raw_input("选择你要操作的服务器组:")
        if chose_server.isdigit():
            chose_server = int(chose_server)
            # 遍历服务器组，将组内主机添加到tmp_server_ip列表中
            for key in server_group.server_ip.get(tmp_milieu[chose_milieu]).get(tmp_server[chose_server]):
                tmp_server_ip.append(key)
        # 遍历tmp_server_ip列表，将ip获取出来
        for index, value in enumerate(tmp_server_ip):
            print index, value
        chose_ip = raw_input("选择你要操作的IP:")
        if chose_ip.isdigit():
            chose_ip = int(chose_ip)
            ip = tmp_server_ip[chose_ip]
        return ip

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
                print "链接超时！！"
            # 发送命令到远程
            child.sendline(command)
            print "-------------------结果为------------------", child.read()
        except pexpect.EOF, err:
            print "EOF-------->", err
        except pexpect.TIMEOUT, err:
            print "TIMEOUT", err
        finally:
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
        interactive.interactive_shell(channel)

        # 关闭连接
        channel.close()
        ssh.close()


if __name__ == "__main__":
    while True:
        way = raw_input("请输入的方式：").strip()
        if way == 'command':
            print "执行一条命令的方式"
            try:
                run = Action()
                ip = run.choseIP()
                command = raw_input("输入要执行的命令：")
                user = raw_input("输入用户名：")
                pwd = getpass.getpass(prompt='输入密码: ')
                run.ssh_command(user, pwd, ip, command)
            except IndexError, err:
                print "你选择的环境/服务器组/主机不存在"
        elif way == 'ssh':
            print "登录到服务器的方式"
            try:
                run = Action()
                ip = run.choseIP()
                user = raw_input("输入用户名：")
                pwd = getpass.getpass(prompt='输入密码: ')
                run.connection(ip, user, pwd)
            except IndexError, err:
                print "你选择的环境/服务器组/主机不存在"
        elif way == 'quit':
            print "----------退出----------"
            break
        else:
            print "--------------------输入的操作方式错误重新输入--------------------"
