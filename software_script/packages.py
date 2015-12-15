#!/usr/bin/env python
# _*_coding:utf-8_*_
#  author:  'Edward.Liu'
# dateTime:  '15/12/9'
#   motto:  'Good memory as bad written'
import datetime, time
import os
import shutil
import subprocess
import tarfile


class Packages(object):
    def __init__(self):
        self.SVN_Checked_Directory = "/install/online/"
        self.Project_Directory_F = "%scybershop-front/target" % self.SVN_Checked_Directory
        self.Project_Directory_B = "%scybershop-web/target" % self.SVN_Checked_Directory
        self.Upload_Directory = "/var/www/html/"
        self.Project_Directory_F_Name = "cybershop-front-0.0.1-SNAPSHOT.war"
        self.Project_Directory_B_Name = "cybershop-web-0.0.1-SNAPSHOT.war"
        self.density_name = ['pro', 'demo', 'ptest']
        self.bulid_home = "/install/maven/bin/mvn"
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H')

    def Subervison_Check(self):
        global SVN_NUMBER
        try:
            while True:
                SVN_NUMBER = raw_input("\033[32mPleae Input SVN Update Number:\033[0m").strip()
                if SVN_NUMBER.isdigit():
                    SVN_NUMBER = int(SVN_NUMBER)
                    if os.path.exists(self.SVN_Checked_Directory):
                        print "------------------------------"
                        os.chdir(self.SVN_Checked_Directory)
                        svn_update = "/usr/bin/svn update -r %s" % SVN_NUMBER
                        subprocess.call(svn_update, shell=True)
                        break
                    else:
                        print "++++++++++++++++++++++++++++++"
                        os.makedirs(self.SVN_Checked_Directory)
                        os.chdir(self.SVN_Checked_Directory)
                        svn_update = "/usr/bin/svn update -r %s" % SVN_NUMBER
                        subprocess.call(svn_update, shell=True)
                        break
                else:
                    print "\033[31mPlease SVN Number\033[0m"
        except KeyboardInterrupt:
            print 'ctrl+d or z'

    def Bulid(self):
        global env
        # 编译项目(分环境)
        # 获取生成项目的文件名-- get
        bulided_File_Path_F = "%s/%s" % (self.Project_Directory_F, self.Project_Directory_F_Name)
        # ---get end
        # 编译环境选择--- select---> Maven
        for index, value in enumerate(self.density_name):
            print index, "Carrefour" + "---->" + value
        try:
            while True:
                Chose_ENV = raw_input("\033[32mChose Density Environment:\033[0m")
                if Chose_ENV.isdigit():
                    Chose_ENV = int(Chose_ENV)
                    env = self.density_name[Chose_ENV]
                    try:
                        if self.density_name[Chose_ENV] == 'pro':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -PcarrefourPro -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                        elif self.density_name[Chose_ENV] == 'demo':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -Pcarrefour -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                        elif self.density_name[Chose_ENV] == 'ptest':
                            os.chdir(self.SVN_Checked_Directory)
                            bulid_command = "%s clean install -PcarrefourPtest -DskipTests" % self.bulid_home
                            subprocess.call(bulid_command, shell=True)
                            if os.path.isfile(bulided_File_Path_F):
                                print "\033[32mBulid %s SuccessFul\033[0m" % self.density_name[Chose_ENV]
                            print "\033[32m--------------------Create TarFiles--------------------\033[0m"
                            self.Files_Handle()
                            break
                    except IndexError:
                        print "\033[31mSelect error\033[0m"
        except KeyboardInterrupt:
            print "\033[32m Quit\033[0m"
            # select----Maven--->END

    def Files_Handle(self):
        # 生成文件处理
        # 文件压缩----tar
        Tmp_density_dir = "/software/%s%s-%s" % (env, SVN_NUMBER, self.date_time)
        os.makedirs(Tmp_density_dir)
        source_fiels = ["%s/%s" % (self.Project_Directory_F, self.Project_Directory_F_Name),
                        "%s/%s" % (self.Project_Directory_B, self.Project_Directory_B_Name)]
        for i in range(2):
            shutil.move(source_fiels[i], Tmp_density_dir)
        # 创建压缩包
        os.chdir("/software")
        tarfile_name = "%s.tar.gz" % Tmp_density_dir.split('/')[2]
        tar = tarfile.open(tarfile_name, "w:gz")
        tar.add(Tmp_density_dir.split('/')[2])
        tar.close()
        # 创建压缩包---end
        if os.path.exists(tarfile_name):
            print "\033[32m----------Delete Temporary Files%s----------\033[0m" % datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S %f')
            shutil.rmtree(Tmp_density_dir)
            shutil.move(tarfile_name, self.Upload_Directory)
            Upload_Files_Name = "%s%s" % (self.Upload_Directory, tarfile_name)
            print "\033[32mSuccessful Download address:http://124.200.96.150:8081/%s\033[0m" % tarfile_name
        else:
            print "\033[31m----------Create archive Is Failed%s----------\033[0m" % datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S %f')
        # 删除临时文件
        print "\033[32m---------Remove the compiled file%s----------\033[0m" % datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S %f')
        if os.path.exists(Upload_Files_Name):
            os.chdir("/software")
            find_tmp = "find %s  -name target" % self.SVN_Checked_Directory
            porc = subprocess.Popen(find_tmp, shell=True, stdout=subprocess.PIPE)
            export, err = porc.communicate()
            out_files = open("path_list.txt", "w")
            out_files.write(export)
            out_files.close()
            fileHandle = open('path_list.txt')
            for line in fileHandle.readlines():
                print "\033[31mRemove Target\033[0m", line
                shutil.rmtree(line.strip('\n'))
            fileHandle.close()
            os.remove("path_list.txt")
            # 删除文件----end

    def usage(self):
        script_name = "packages.py"
        print "\033[31m*****************************************\033[0m"
        print "\033[31m|------------Packages Useage------------|\033[0m"
        print "\033[32m|------------./%s--------------|\033[0m" % script_name
        print "\033[32m|------------<path>/%s---------|\033[0m" % script_name
        print "\033[32m|----------脚本执行过程2部人工干预------|\033[0m"
        print "\033[32m|----------1.收到输入 SVN 版本号--------|\033[0m"
        print "\033[32m|----------2.选择需要打包的环境---------|\033[0m"
        print "\033[32m|----------3.复制输出下载链接进行下载---|\033[0m"
        print "\033[31m******************************************\033[0m"


if __name__ == '__main__':
    Run_packages = Packages()
    Run_packages.usage()
    Run_packages.Subervison_Check()
    Run_packages.Bulid()
