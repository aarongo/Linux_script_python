#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# _*_coding:utf-8_*_
__author__ = 'yulong'

import paramiko

import interactive

dic = {
    "environment1": {
        "ip": ['172.31.1.160', '172.31.1.101', '172.31.1.100', '172.31.1.200'],
        "user_info": ('root', 'comall2014')
    },
    "environment2": {
        "ip": ['10.90.6.25', '10.90.6.26', '10.90.6.27', '10.90.6.28', '10.90.6.29', '10.90.6.30', '10.90.6.31',
               '10.90.6.32', '10.90.6.33', '10.90.6.34'],
        "user_info": ('root', 'PASSWORD')
    }
}


class itrem2(object):
    def get_remote_info(self):
        environment_tmp = []
        environment_ip = None
        user_info = None
        ip = None
        for key in dic:
            environment_tmp.append(key)
        while True:
            try:
                for index, value in enumerate(environment_tmp):
                    print index, value
                chose_environment = raw_input("\033[32mPlease Chose Environment:\033[0m").strip()
                if chose_environment.isdigit():
                    chose_environment = int(chose_environment)
                    environment_ip = dic[environment_tmp[chose_environment]].get('ip')
                    user_info = dic[environment_tmp[chose_environment]].get('user_info')
                    break
            except IndexError, err:
                print "\033[31m**********Input Error**********\033[0m"
        while True:
            try:
                for x, v in enumerate(environment_ip):
                    print x, v
                chose_environment_ip = raw_input("\033[32mPlease Chose Ip:\033[0m").strip()
                if chose_environment_ip.isdigit():
                    chose_environment_ip = int(chose_environment_ip)
                    ip = environment_ip[chose_environment_ip]
                return ip, user_info
                break
            except IndexError, err:
                print "\033[31m**********Input Error**********\033[0m"

                # 登录shell到远程服务器

    def connection(self, ip, user, password, port=22):
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


if __name__ == "__main__":
    start = itrem2()
    tmp = start.get_remote_info()
    if tmp != 0:
        print "Ip地址为：", tmp[0]
        print "用户为：", tmp[1][0]
        print "密码为：", tmp[1][1]
        start.connection(tmp[0], tmp[1][0], tmp[1][1])
    else:
        print "\033[31m***************Get Ip And User_info Failed**************\033[0m"
