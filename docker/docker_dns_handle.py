#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/8'
#   motto:  'Good memory as bad written'


import subprocess
import sys
import time


# docker 启动 DNS

class DnsHandle(object):
    def start_dns(self):
        # 调取Docker 命令启动 dns 镜像
        dns_images_name = "www.edward-001.com:5000/skydns"
        dns_start_name = "skydns"
        dns_start_domain = "docker"
        dns_start_nameserver = "8.8.8.8:53"
        # 启动 Docker 容器 dns
        command_line1 = "docker run -d -p 172.17.42.1:53:53/udp -p 8080:8080 --name %s %s -nameserver %s  -domain %s" % (
            dns_start_name, dns_images_name, dns_start_nameserver, dns_start_domain)
        print "\033[32m--------------------Start Skydns---------------------\033[0m"
        subprocess.call(command_line1, shell=True)
        # 启动 Docker 容器服务自发现服务
        discovery_images_name = "www.edward-001.com:5000/skydock"
        discovery_start_name = "skydock"
        discovery_start_environment = "edward-dev"
        discovery_mount_floum = "/var/run/docker.sock:/docker.sock"

        command_line2 = "docker run -d -v %s --name %s %s  -ttl 30 -environment %s -s /docker.sock -domain %s -name %s" % (
            discovery_mount_floum, discovery_start_name, discovery_images_name, discovery_start_environment,
            dns_start_domain, dns_start_name)
        print "\033[32m----------------Start Skydock------------------\033[0m"
        subprocess.call(command_line2, shell=True)
        # 检查服务是否启动
        command_line3 = "docker ps | grep -v 'CONTAINER ID' | awk '{print $1}' | wc -l"
        p = subprocess.Popen(command_line3, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if out >= 2:
            print "\033[32m-----------Start DNS Sucessful----------\033[0m"
        else:
            print "\033[31m-----------Start DNS Failed--------------\033[0m"

    def stop_dns(self):
        # 停止 dns 并且删除遗留镜像
        command_line1 = "docker ps | grep sky | awk '{print $1}'"
        d = subprocess.Popen(command_line1, shell=True, stdout=subprocess.PIPE)
        out, err = d.communicate()
        print "\033[32m-------------Stop Docker DNS-------------\033[0m"
        for value in out.split():
            command_line2 = "docker stop %s && docker rm %s " % (value, value)
            print "\033[32m-----------Start Command %s--------------\033[0m" % command_line2
            subprocess.call(command_line2, shell=True)
            time.sleep(3)

    def restart_dns(self):
        # GET CONTAINER ID
        command_line1 = "docker ps | grep sky | awk '{print $1}'"
        d = subprocess.Popen(command_line1, shell=True, stdout=subprocess.PIPE)
        out, err = d.communicate()
        # 重新启动 Docker_dns
        print "\033[32m-----------------Restart Docker DNS-----------------\033[0m"
        for contatinerID in out.split():
            command_line2 = "docker  restart --time=10 %s" % contatinerID
            print "\033[32m---------------Restart contatinerId:%s--------------------\033[0m" % contatinerID
            subprocess.call(command_line2, shell=True)
            time.sleep(5)


if __name__ == "__main__":
    Handle = DnsHandle()
    try:
        if sys.argv[1] == 'start':
            Handle.start_dns()
        elif sys.argv[1] == 'stop':
            Handle.stop_dns()
        elif sys.argv[1] == 'restart':
            Handle.restart_dns()
    except IndexError, err:
        print "\033[31m----------Please Input Parameters----------\033[0m"
