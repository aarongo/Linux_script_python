# _*_coding:utf-8_*_
__author__ = 'yulong'

'''
    家乐福生产环境部署脚本 V1
'''
import subprocess, datetime, os


class Carrefour(object):
    def down(self):
        global pwd, url, tar_name, directory_name
        pwd = "/software/deploybak/"
        url = str(raw_input("Please Input Download Url:"))
        # 转换输入的url为列表以（/）分割
        way = "cd %s && wget  %s" % (pwd, url)
        tar_name = url.split("/")[3]
        # 解压后的目录名称
        directory_name = tar_name.split(".")[0]
        print "Running programs.............."
        load = subprocess.Popen(way, shell=True)
        load.wait()
        if load.returncode == 0:
            print "--------DownLoad File Sueccessful--------"
        else:
            print "--------DownLoad tar file Fail--------"

    def extract(self):
        extract_command = "cd %s && tar xzf %s" % (pwd, tar_name)
        print "Extract DownLoad Tar File.................."
        extract_comm = subprocess.Popen(extract_command, shell=True)
        extract_comm.wait()
        if extract_comm.returncode == 0:
            print "--------解压tar包成功--------"
        else:
            print "--------解压tar包失败--------"

    def transfer(self):
        server_address = ["172.31.0.252", "172.31.0.253"]
        remote_directory = "/software"
        for i in range(len(server_address)):
            command_scp = "cd  %s/%s && scp *  root@%s:%s  " % (
                pwd, directory_name, server_address[i], remote_directory)
            run_scp = subprocess.Popen(command_scp, shell=True)
            run_scp.wait()
            if run_scp.returncode == 0:
                print "--------Scp *.war Sucessful--------"
            else:
                print "--------Scp *.war Fail--------"


if __name__ in "__main__":
    down = Carrefour()
    down.down()
    down.extract()
    down.transfer()
