#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'lonny'
# dateTime:  '15/12/7'
#   motto:  'Good memory as bad written'
import platform
#
# print 'Version      :', platform.python_version()
# print 'Version tuple:', platform.python_version_tuple()
# print 'Compiler     :', platform.python_compiler()
# print 'Build        :', platform.python_build()
#
# print "------------------------------------"
#
# print 'Normal :', platform.platform()
# print 'Aliased:', platform.platform(aliased=True)
# print 'Terse  :', platform.platform(terse=True)
#
# print "------------------------------------"
#
# print 'uname:', platform.uname()
#
# print
# print 'system   :', platform.system()
# print 'node     :', platform.node()
# print 'release  :', platform.release()
# print 'version  :', platform.version()
# print 'machine  :', platform.machine()
# print 'processor:', platform.processor()
# print "-----------------------------"
#
# print 'interpreter:', platform.architecture()
# print '/bin/ls    :', platform.architecture('/bin/ls')


import datetime
import os
import shutil
import subprocess


class Packages(object):
    def __init__(self):
        self.SVN_Checked_Directory = "/install/online/"
        self.Project_Directory_F = "%scybershop-front/target" % self.SVN_Checked_Directory
        self.Project_Directory_B = "%scybershop-web/target" % self.SVN_Checked_Directory
        self.Upload_Directory = "/var/www/html/"
        self.Project_Directory_F_Name = "cybershop-front-0.0.1-SNAPSHOT.war"
        self.Project_Directory_B_Name = "cybershop-front-0.0.1-SNAPSHOT.war"
        self.density_name = ['pro', 'demo', 'ptest']
        self.bulid_home = "/install/maven/bin/mvn"
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H')

    def Subervison_Check(self):
        global SVN_NUMBER
        SVN_NUMBER = raw_input("\033[32mPleae Input SVN Update Number:\033[0m").strip()


    def Bulid(self):
        # 编译项目(分环境)
        # 获取生成项目的文件名-- get
        bulided_File_Path_F = "%s/%s" % (self.Project_Directory_F, self.Project_Directory_F_Name)
        # ---get end
        # 编译环境选择--- select---> Maven
        for index, value in enumerate(self.density_name):
            print index, value
        try:
            while True:
                Chose_ENV = raw_input("\033[32mChose Density Environment:\033[0m")
                if Chose_ENV.isdigit():
                    Chose_ENV = int(Chose_ENV)
                    try:
                        if self.density_name[Chose_ENV] == 'carrefour_pro':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -PcarrefourPro -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            Tmp_density_dir = "/software/%s%s-%s" % (self.density_name[Chose_ENV], SVN_NUMBER, self.date_time)


                            break
                        elif self.density_name[Chose_ENV] == 'carrefour_demo':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -Pcarrefour -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            break
                        elif self.density_name[Chose_ENV] == 'carrefour_ptest':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -PcarrefourPtest -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            break
                    except IndexError:
                        print "\033[31mSelect error\033[0m"
        except KeyboardInterrupt:
            print "\033[32m Quit\033[0m"
            # select----Maven--->END
        # 创建临时存放文件夹




if __name__ == '__main__':
    Run_packages = Packages()
    Run_packages.Subervison_Check()
    Run_packages.Density_Move()
