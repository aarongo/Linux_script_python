#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/10/26'
#   motto:  'Good memory as bad written'

import os
import subprocess


class AutoNginx(object):
    # 获取依赖库等
    depend_path = os.path.split(os.path.realpath(__file__))[0]
    pcre_name = 'pcre-8.36.tar.gz'
    openssl_name = 'openssl-1.0.0s.tar.gz'
    zlib_name = 'zlib-1.2.8.tar.gz'
    pcre_path_info = "%s/%s" % (depend_path, pcre_name)
    openssl_path_info = "%s/%s" % (depend_path, openssl_name)
    zlib_path_info = "%s/%s" % (depend_path, zlib_name)
    # end

    def optcions(self):
        compiler_optcions = """ --user=nginx --group=nginx\\
                --with-http_ssl_module --with-http_gunzip_module --with-http_gzip_static_module\\
                --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module\\
                --with-http_auth_request_module --with-file-aio """

        # add optcions
        compiler_optcions += '--with-pcre=%s --with-zlib=%s --with-openssl=%s' % (
            self.pcre_path_info.split('.tar.gz')[0], self.zlib_path_info.split('.tar.gz')[0],
            self.openssl_path_info.split('.tar.gz')[0])
        return compiler_optcions

    def depend(self):
        # 解压depend 文件
        # pcre
        command_line1 = "tar xzf %s -C %s && cd %s && ./configure && make && make install" % (
            self.pcre_path_info, self.depend_path, self.pcre_path_info.split('.tar.gz')[0])
        # zlib
        command_line2 = "tar xzf %s -C %s && cd %s && ./configure && make && make install" % (
            self.zlib_path_info, self.depend_path, self.zlib_path_info.split('.tar.gz')[0])
        # openssl
        command_line3 = "tar xzf %s -C %s && cd %s && ./config && make && make install" % (
            self.openssl_path_info, self.depend_path, self.openssl_path_info.split('.tar.gz')[0])
        print "\033[32m Decompression Depend software \033[0m"
        subprocess.call(command_line1, shell=True)
        subprocess.call(command_line2, shell=True)
        subprocess.call(command_line3, shell=True)

    def install_tengine(self):
        print "\033[32m Install Tengine.......\033[0m"
        if os.path.exists(self.pcre_path_info.split('.tar.gz')[0]) and os.path.exists(
                self.zlib_path_info.split('.tar.gz')[0]) and os.path.exists(self.openssl_path_info.split('.tar.gz')[0]):
            print "\033[32m Depend Is Exists Install Tengin\033[0m"
            tengine_base_default = "/software/tengine"
            tengine_path = raw_input("Please Input Tengine Install Dir:").strip()
            if len(tengine_path) == 0:
                tengine_path = tengine_base_default
                optcions = "--prefix=%s %s" % (tengine_path, self.optcions())
                tengine_package_path = "%s/tengine-2.1.1.tar.gz" % self.depend_path
                command_line1 = "tar xzf %s -C %s " % (tengine_package_path, self.depend_path)
                command_line2 = "cd %s && ./configure %s && make && make install" % (
                    tengine_package_path.split('.tar.gz')[0], optcions)
                subprocess.call(command_line1, shell=True)
                subprocess.call(command_line2, shell=True)
                if os.path.exists(tengine_path):
                    print "\033[32m Tengine-2.1.1 Install Successful\033[0m"
                else:
                    print "\033[31m Tengine-2.1.1 Install Failed\033[0m"
            else:
                tengine_base_default = tengine_path
                optcions = "%s %s" % (tengine_base_default, self.optcions())
                tengine_package_path = "%s/tengine-2.1.1.tar.gz"
                command_line1 = "tar xzf %s -C %s " % (tengine_package_path, self.depend_path)
                command_line2 = "cd %s && ./configure %s && make && make install" % (
                    tengine_package_path.split('.tar.gz')[0], optcions)
                subprocess.call(command_line1, shell=True)
                subprocess.call(command_line2, shell=True)
        else:
            print "\033[32 Depend Is Not Exists \033[0m"

    def install_nginx(self):
        print "\033[32m Install Nginx.......\033[0m"
        if os.path.exists(self.pcre_path_info.split('.tar.gz')[0]) and os.path.exists(
                self.zlib_path_info.split('.tar.gz')[0]) and os.path.exists(self.openssl_path_info.split('.tar.gz')[0]):
            print "\033[32m Depend Is Exists Install nginx\033[0m"
            tengine_base_default = "/software/Nginx"
            tengine_path = raw_input("Please Input Nginx Install Dir:").strip()
            if len(tengine_path) == 0:
                tengine_path = tengine_base_default
                optcions = "--prefix=%s %s" % (tengine_path, self.optcions())
                tengine_package_path = "%s/nginx-1.8.0.tar.gz" % self.depend_path
                command_line1 = "tar xzf %s -C %s " % (tengine_package_path, self.depend_path)
                command_line2 = "cd %s && ./configure %s && make && make install" % (
                    tengine_package_path.split('.tar.gz')[0], optcions)
                subprocess.call(command_line1, shell=True)
                subprocess.call(command_line2, shell=True)
                if os.path.exists(tengine_path):
                    print "\033[32m nginx-1.8.0 Install Successful\033[0m"
                else:
                    print "\033[31m nginx-1.8.0 Install Failed\033[0m"
            else:
                tengine_base_default = tengine_path
                optcions = "%s %s" % (tengine_base_default, self.optcions())
                tengine_package_path = "%s/nginx-1.8.0.tar.gz"
                command_line1 = "tar xzf %s -C %s " % (tengine_package_path, self.depend_path)
                command_line2 = "cd %s && ./configure %s && make && make install" % (
                    tengine_package_path.split('.tar.gz')[0], optcions)
                subprocess.call(command_line1, shell=True)
                subprocess.call(command_line2, shell=True)
        else:
            print "\033[32 Depend Is Not Exists \033[0m"


if __name__ == "__main__":
    chose_list = ['Tengine', 'Nginx']
    while True:
        for index, value in enumerate(chose_list):
            print index, value
        chose = raw_input("Please Chose Install:")
        try:
            if chose.isdigit():
                chose = int(chose)
                if chose_list[chose] == chose_list[0]:
                    tengine = AutoNginx()
                    tengine.depend()
                    tengine.install_tengine()
                    break
                elif chose_list[chose] == chose_list[1]:
                    nginx = AutoNginx()
                    nginx.depend()
                    nginx.install_nginx()
                    break
        except IndexError, err:
            print "\033[31m You Chose Is Error Please Try Agin\033[0m"
