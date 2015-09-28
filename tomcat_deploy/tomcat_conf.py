#!/usr/bin/python
# _*_coding:utf-8_*_


"""
15-9-22
author : 'yulong'
Good memory than rotten written
"""
# bulid 选项
svn_bin_home = "/usr/bin/svn"
svn_checkout_dir = "/install/cybershop-B2B2C-test/"
maven_bin_home = "/install/maven/bin/mvn"
# 临时解压 war 包文件夹
unzip_tmp = "/install/unzip_tmp"
unzip_war_front = "/install/unzip_tmp/cybershop-front-0.0.1-SNAPSHOT"
unzip_war_web = "/install/unzip_tmp/cybershop-web-0.0.1-SNAPSHOT"
war_path = ["/install/cybershop-B2B2C-test/cybershop-front/target/",
            "/install/cybershop-B2B2C-test/cybershop-web/target/"]
# 远程主机
remote_host_dir = {
    '172.31.1.100': '/root/war_test/',
    '172.31.1.101': '/root/war_test/'
}
