#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/11/24'
#   motto:  'Good memory as bad written'

import time, os
import subprocess
import psutil


class File_Handle(object):
    def __init__(self, download_home, download_url, unzip_home, send_front_list=['10.90.10.246', '10.90.10.247'],
                 send_web_list=['10.90.10.246', '10.90.10.247'], remote_front='/software/deploy_front',
                 remote_backend='/software/deploy_backend',
                 deploy_file_name_front="cybershop-front-0.0.1-SNAPSHOT.war",
                 deploy_file_name_backend="cybershop-web-0.0.1-SNAPSHOT.war"):
        self.download_home = download_home
        self.download_url = download_url
        self.unzip_home = unzip_home
        self.send_front_list = send_front_list
        self.send_web_list = send_web_list
        self.remote_front = remote_front
        self.remote_backend = remote_backend
        self.deploy_file_name_front = deploy_file_name_front
        self.deploy_file_name_backend = deploy_file_name_backend

    def download_file(self):
        # download deploy files
        download_command = "wget %s -P %s " % (self.download_url, self.download_home)
        subprocess.call(download_command, shell=True)
        download_file_name = "%s/%s" % (self.download_home, self.download_url.split('/')[3])
        if os.path.exists(download_file_name):
            print "\033[32m DownLoad Files SuccessFul FileName is %s\033[0m" % self.download_url.split('/')[3]
        else:
            print "\033[31m DownLoad Files Failed \033[0m"
            # download end

    def files_handle(self):
        # handle deploy files
        unzip_file = "tar xzf %s/%s -C %s" % (self.download_home, self.download_url.split('/')[3], self.download_home)
        unzip_front_file = "unzip %s/%s/%s -d %s/%s >/dev/null  2>&1" % (
            self.download_home, self.download_url.split('/')[3].split('.tar.gz')[0], self.deploy_file_name_front,
            self.unzip_home, self.deploy_file_name_front.split('.war')[0])
        unzip_web_file = "unzip %s/%s/%s -d %s/%s >/dev/null  2>&1" % (
            self.download_home, self.download_url.split('/')[3].split('.tar.gz')[0], self.deploy_file_name_backend,
            self.unzip_home, self.deploy_file_name_backend.split('.war')[0])
        # running
        subprocess.call(unzip_file, shell=True)
        subprocess.call(unzip_front_file, shell=True)
        subprocess.call(unzip_web_file, shell=True)

    def send_files_front(self):
        # send front files
        print "\033[32m Start Front Send Files %s\033[0m" % (time.strftime("%Y-%m-%d %H:%M:%S"))
        for addr in self.send_front_list:
            scp_command = "scp -r %s/%s %s:%s >/dev/null  2>&1" % (
                self.unzip_home, self.deploy_file_name_front.split('.war')[0], addr, self.remote_front)
            subprocess.call(scp_command, shell=True)
        print "\033[32m Front Send Files End %s \033[0m" % (time.strftime("%Y-%m-%d %H:%M:%S"))

    def send_files_web(self):
        # send web files
        print "\033[32m Start Send Backend Files %s\033[0m" % (time.strftime("%Y-%m-%d %H:%M:%S"))
        for addr in self.send_web_list:
            scp_command = "scp -r %s/%s %s:%s >/dev/null  2>&1" % (
                self.unzip_home, self.deploy_file_name_backend.split('.war')[0], addr, self.remote_backend)
            subprocess.call(scp_command, shell=True)
        print "\033[32m Backend Send Files End %s \033[0m" % (time.strftime("%Y-%m-%d %H:%M:%S"))


class Front(object):
    def __init__(self, send_front_list=['10.90.10.246', '10.90.10.247'], send_web_list=['10.90.10.246', '10.90.10.247'],
                 Tomcat_Home="-Dcatalina.base=/install/tomcat-mobile"):
        self.Tomcat_Home = Tomcat_Home
        self.send_front_list = send_front_list
        self.send_web_list = send_web_list

    def start_tomcat(self):
        # Start Front Tomcat
        tomcat_bin_path = "%s/bin/startup.sh" % self.Tomcat_Home.split('=')[1]
        for addr in self.send_front_list:
            # start_tomcat = "ssh %s '%s/bin/startup.sh'" % (addr,)
            p = psutil.Popen(tomcat_bin_path, stdout=subprocess.PIPE)
            # subprocess.call(start_tomcat, shell=True)
            print start_tomcat

    def stop_tomcat(self):
        # Stop Front Tomcat
        for p in psutil.process_iter():
            try:
                if p.name() == 'java':
                    for options in p.cmdline():
                        if self.Tomcat_Home == options:
                            stop_tomcat = p.kill
                            print "\033[32m Tomcat_mobile Process is Running\033[0m"
            except psutil.Error:
                print psutil.Error

    def restart_tomcat(self):
        pass

    def create_static_soft(self):
        pass

    def create_img_soft(self):
        pass

    def remove_soft(self):
        pass


class Backend(object):
    def __init__(self):
        pass

    def start_tomcat(self):
        pass

    def stop_tomcat(self):
        pass

    def restart_tomcat(self):
        pass

    def create_static_soft(self):
        pass

    def create_img_soft(self):
        pass

    def remove_soft(self):
        pass


if __name__ == '__main__':
    # download url http://124.200.96.150:8081/ptest2015-11-19-23-14316.tar.gz
    download_url = raw_input("Please DownLoad Urls:").strip()
    handle_files = File_Handle("/software/backwar", download_url, "/software/unzip")
    # handle_files.download_file()
    # handle_files.files_handle()
    # handle_files.send_files_front()
    # handle_files.send_files_web()
    tomcat_handle = Front()
    tomcat_handle.start_tomcat()
    tomcat_handle.stop_tomcat()
