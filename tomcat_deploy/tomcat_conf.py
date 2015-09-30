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
project_dir = "/install/unzip_project"
unzip_war_front = "%s/cybershop-front-0.0.1-SNAPSHOT" % project_dir
unzip_war_web = "%s/cybershop-web-0.0.1-SNAPSHOT" % project_dir
war_path = ["/install/cybershop-B2B2C-test/cybershop-front/target/",
            "/install/cybershop-B2B2C-test/cybershop-web/target/"]
# 远程主机 将此目录里的项目目录连接到 tomcat 部署目录中
remote_host_dir = {
    # '172.31.1.100': '/install/cybershop_project/',
    # '172.31.1.101': '/install/cybershop_project/'
    '10.90.10.169': '/install/cybershop_project/'
}
remote_host_user = 'root'
remote_host_password = 'comall2014'

