# _*_coding:utf-8_*_
import pexpect

server_ip = ['10.90.6.28', '10.90.6.29', '10.90.6.30']
server_ip_user = 'root'
server_ip_passwd = 'PASSWORD'
cmd = "ps aux | grep memcached | grep -v grep | awk '{print $2}'"


def memcached():
    print "------memcahced server List------"
    while True:
        for index, ip in enumerate(server_ip):
            print index, ip
        server = raw_input("请输入你要操作的服务器：").strip()
        if server.isdigit():
            server = int(server)
            print "您要操作的为服务器为：", server_ip[server]



memcached()
