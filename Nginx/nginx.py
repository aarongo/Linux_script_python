#!/usr/bin/python
# _*_coding:utf-8_*_
# __author__ = 'yulong'
# Good memory than rotten written
import subprocess
import sys, os
import ConfigParser


class Nginx(object):
    conf = ConfigParser.ConfigParser()
    conf.read('Nginx_conf.ini')
    # 查看nginx进程
    def check_nginx_process(self):
        # 运行查看Linux Nginx进程
        command = "%s" % (self.conf.get('global', 'nginx_process'))
        print "\033[32m########################Nginx Process########################\033[0m"
        subprocess.call(command, shell=True)
        print "\033[32m#########################################################\033[0m"

    # 启动Nginx
    def start_nginx(self):
        # 启动Nginx
        command = "%s %s %s" % (
            self.conf.get('global', 'nginx_bin_home'), self.conf.get('global', 'nginx_start_options'),
            self.conf.get('global', 'nginx_config'))
        print "\033[32m########################Nginx Starting########################\033[0m"
        start_nginx = subprocess.Popen(command, shell=True)
        start_nginx.wait()
        '''
            启动需要进行判断,因为关闭掉nginx后nginx.pid不会删除,会保留上一次的pid
        '''
        # 获取nginx.pid的值
        # 存放临时取出的pid
        files_pid = []
        run_pid = []
        # 获取pid文件中的值存放到files_pid中
        command_files_pid = "%s" % (self.conf.get('global', 'nginx_process_pid'))
        outs = subprocess.Popen(command_files_pid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in outs.stdout.readlines():
            files_pid.append(line.strip())
        # 获取正在运行的PID存放到run_pid中
        command_running_pid = "%s" % (self.conf.get('global', 'nginx_get_runing_pid'))
        outs_pid = subprocess.Popen(command_running_pid, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        for line in outs_pid.stdout.readlines():
            run_pid.append(line.strip())
        # 进行判断文件中的Pid是否存在与正在运行的pid中
        try:
            if files_pid[0] in run_pid:
                print "\033[32m----------Staring Nginx Successful----------\033[0m"
            else:
                print "\033[31m----------Staring Nginx Failed----------\033[0m"
        except IndexError:
            print "\033[31m----------The Server Is Not Exist----------\033[0m"

    # 平滑重启Ningx
    def reload_nginx(self):
        command_reload = "%s %s" % (self.conf.get('global', 'nginx_bin_home'), self.conf.get('global', 'nginx_reload'))
        print "\033[32m########################Nginx Reload########################\033[0m"
        subprocess.call(command_reload, shell=True)
        print "\033[32m#########################################################\033[0m"

    # 停止Ningx,处理完当前请求后进行重启
    def stop_nginx(self):
        command_stop_request = "%s" % (self.conf.get('global', 'nginx_normal_stop'))
        print "\033[32m########################Nginx Stop(Request)########################\033[0m"
        request = subprocess.Popen(command_stop_request, shell=True)
        print "\033[32mStoping............."
        request.wait()
        if request.returncode == 0:
            print "\033[32m---------Stop Nginx Successful---------\033[0m"
        else:
            print "\033[31m---------Stop Nginx Failed-------------\033[0m"

    # 快速停止Nginx
    def fast_stop_nginx(self):
        command_Fast = "%s" % (self.conf.get('global', 'nginx_fast_stop'))
        print "\033[32m########################Nginx Fast Stop########################\033[0m"
        fast_stop = subprocess.Popen(command_Fast, shell=True)
        fast_stop.wait()
        if fast_stop.returncode == 0:
            print "\033[32m Fast Stop Nginx Successful\033[0m"
        else:
            print "\033[32m Fast Stop Nginx Failed\033[0m"
        print "\033[32m#########################################################\033[0m"

    # 显示Nginx的配置文件内容
    def view_nginx_conf(self):
        # 显示Nginx的配置文件内容
        command = "%s %s" % (self.conf.get('global', 'nginx_bin_home'), (self.conf.get('global', 'nginx_conf_view')))
        print "\033[32m########################配置文件为########################\033[0m"
        subprocess.call(command, shell=True)
        print "\033[32m#########################################################\033[0m"

    # 检测Ningx配置文件
    def check_nginx_conf(self):
        # 检测nginx的完整配置信息
        command = "%s %s %s" % (self.conf.get('global', 'nginx_bin_home'), self.conf.get('global', 'nginx_config_test'),
                                self.conf.get('global', 'nginx_config'))
        print "\033[32m########################检测结果为########################\033[0m"
        subprocess.call(command, shell=True)
        print "\033[32m#########################################################\033[0m"

    # 查看Ningx所有信息
    def check_nginx_info(self):
        # 查看nginx完整配置信息
        command = "%s %s" % (self.conf.get('global', 'nginx_bin_home'), self.conf.get('global', 'nginx_info'))
        print "\033[32m########################Nginx Info########################\033[0m"
        subprocess.call(command, shell=True)
        print "\033[32m##########################################################\033[0m"
        # ip地址列表

    # 统计Nginx日志内的访问IP
    def nginx_accessnum(self):
        dir = "%s" % self.conf.get('global', 'Nginx_logs_path')
        files = os.listdir(dir)
        print "\033[32m*******************日志目录下的文件内容为*******************\033[0m"
        for f in files:
            print dir + os.sep + f
        # ip地址列表
        ip_list = []
        log_pat = raw_input("Please Input Logs Path:").strip()
        command_num = "cat %s  | awk '{print $1,$6}' > list.txt" % log_pat
        command = subprocess.Popen(command_num, shell=True)
        command.wait()
        f = file("list.txt", "r")
        for line in f.readlines():
            ip_list.append(line.strip())
        print "\033[31m Nginx总的访问次数为：\033[0m", len(ip_list), "\n"
        # 首先遍历set集合，以遍历到的元素为值传给统计列表函数
        # 首先转换ip_list类型
        ip_set = set(ip_list)
        access_max = int(raw_input("请输入你过滤的访问次数："))
        print "\033[32m超过 %s 次访问的IP \033[0m --------\033[32m 访问次服务器的次数为：\033[0m" % access_max
        for item in ip_set:
            if ip_list.count(item) > access_max:
                print item, "--------------------", ip_list.count(item)
        f.close()


if __name__ == "__main__":
    help_com = """\033[32m
            ps:查看Nginx当前进程
         start:启动Nginx服务
        reload:平滑重启Nginx服务（重新读取配置文件）
          stop:停止Nginx服务（处理完当前的请求后关闭Ningx）
          kill:×快速停止Nginx服务（不保存相关信息）
      v_config:显示Nginx配置文件
          test:测试Nginx配置文件
             -V:显示Nginx的所有信息
         access:统计访问日志的ip\033[0m
        """
    run = Nginx()
    if sys.argv[1] == 'ps':
        run.check_nginx_process()
    elif sys.argv[1] == 'start':
        run.start_nginx()
    elif sys.argv[1] == 'reload':
        run.reload_nginx()
    elif sys.argv[1] == 'stop':
        run.stop_nginx()
    elif sys.argv[1] == 'kill':
        run.fast_stop_nginx()
    elif sys.argv[1] == 'v_config':
        run.view_nginx_conf()
    elif sys.argv[1] == 'test':
        run.check_nginx_conf()
    elif sys.argv[1] == '-V':
        run.check_nginx_info()
    elif sys.argv[1] == 'access':
        run.nginx_accessnum()
    elif sys.argv[1] == '--help':
        print help_com
